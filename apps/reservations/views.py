from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from apps.services.models import Service
from apps.team.models import Masseuse

from .forms import (
    Step1ServiceForm,
    Step2MasseuseForm,
    Step3DateTimeForm,
    Step4ContactForm,
    get_available_dates,
    get_available_times,
)
from .models import Reservation, TimeSlot

SESSION_KEY = 'reservation_wizard'


def _get_wizard(request):
    return request.session.get(SESSION_KEY, {})


def _set_wizard(request, data):
    wizard = _get_wizard(request)
    wizard.update(data)
    request.session[SESSION_KEY] = wizard
    request.session.modified = True


def _clear_wizard(request):
    request.session.pop(SESSION_KEY, None)


class ReservationWizardView(RedirectView):
    permanent = False
    pattern_name = 'core:home'


class WizardStepView(View):
    step_templates = {
        1: 'partials/htmx/reservation_step1.html',
        2: 'partials/htmx/reservation_step2.html',
        3: 'partials/htmx/reservation_step3.html',
        4: 'partials/htmx/reservation_step4.html',
        5: 'partials/htmx/reservation_step5.html',
    }

    def post(self, request, step):
        step = int(step)
        wizard = _get_wizard(request)

        if step == 1:
            form = Step1ServiceForm(request.POST)
            if form.is_valid():
                service = form.cleaned_data['service']
                _set_wizard(request, {'service_id': service.pk, 'step': 2})
                return self._render_step(request, 2)
            return self._render_step(request, 1, form=form)

        if step == 2:
            form = Step2MasseuseForm(request.POST)
            if form.is_valid():
                masseuse = form.cleaned_data['masseuse']
                _set_wizard(request, {
                    'masseuse_id': masseuse.pk if masseuse else None,
                    'step': 3,
                })
                return self._render_step(request, 3)
            return self._render_step(request, 2, form=form)

        if step == 3:
            masseuse = None
            if wizard.get('masseuse_id'):
                masseuse = Masseuse.objects.filter(pk=wizard['masseuse_id']).first()
            form = Step3DateTimeForm(request.POST, masseuse=masseuse)
            if form.is_valid():
                slot = form.cleaned_data['time_slot']
                _set_wizard(request, {
                    'time_slot_id': slot.pk,
                    'slot_date': str(slot.date),
                    'slot_time': str(slot.time),
                    'step': 4,
                })
                return self._render_step(request, 4)
            return self._render_step(request, 3, form=form)

        if step == 4:
            form = Step4ContactForm(request.POST)
            if form.is_valid():
                _set_wizard(request, {
                    'name': form.cleaned_data['name'],
                    'email': form.cleaned_data['email'],
                    'phone': form.cleaned_data['phone'],
                    'notes': form.cleaned_data.get('notes', ''),
                    'step': 5,
                })
                return self._render_step(request, 5)
            return self._render_step(request, 4, form=form)

        return HttpResponse(status=400)

    def get(self, request, step):
        return self._render_step(request, int(step))

    def _render_step(self, request, step, form=None):
        wizard = _get_wizard(request)
        wizard['step'] = step
        request.session[SESSION_KEY] = wizard

        context = {
            'wizard_step': step,
            'wizard': wizard,
            'step_labels': [_('Služba'), _('Masérka'), _('Termín'), _('Kontakt'), _('Potvrzení')],
        }

        if step == 1:
            context['form'] = form or Step1ServiceForm()
            context['services'] = Service.objects.filter(is_active=True)
        elif step == 2:
            context['form'] = form or Step2MasseuseForm()
            context['masseuses'] = Masseuse.objects.filter(is_active=True)
            context['selected_service'] = Service.objects.filter(pk=wizard.get('service_id')).first()
        elif step == 3:
            masseuse = Masseuse.objects.filter(pk=wizard.get('masseuse_id')).first()
            context['form'] = form or Step3DateTimeForm(masseuse=masseuse)
            context['available_dates'] = get_available_dates(masseuse)
            context['available_times'] = get_available_times()
            context['selected_masseuse'] = masseuse
        elif step == 4:
            context['form'] = form or Step4ContactForm()
            context['summary'] = self._build_summary(wizard)
        elif step == 5:
            context['summary'] = self._build_summary(wizard)

        template = self.step_templates[step]
        return render(request, template, context)

    def _build_summary(self, wizard):
        service = Service.objects.filter(pk=wizard.get('service_id')).first()
        masseuse = Masseuse.objects.filter(pk=wizard.get('masseuse_id')).first()
        slot = TimeSlot.objects.filter(pk=wizard.get('time_slot_id')).first()
        return {
            'service': service,
            'masseuse': masseuse,
            'slot': slot,
            'name': wizard.get('name'),
            'email': wizard.get('email'),
            'phone': wizard.get('phone'),
            'notes': wizard.get('notes', ''),
        }


class ConfirmReservationView(View):
    def post(self, request):
        wizard = _get_wizard(request)
        if not all(k in wizard for k in ('service_id', 'time_slot_id', 'name', 'email', 'phone')):
            return redirect('reservations:wizard')

        service = Service.objects.get(pk=wizard['service_id'])
        slot = TimeSlot.objects.get(pk=wizard['time_slot_id'])
        masseuse = Masseuse.objects.filter(pk=wizard.get('masseuse_id')).first()

        if slot.is_booked:
            return render(request, 'partials/htmx/reservation_error.html', {
                'message': _('Tento termín je již obsazený. Vyberte prosím jiný.'),
            }, status=409)

        reservation = Reservation.objects.create(
            service=service,
            masseuse=masseuse,
            time_slot=slot,
            name=wizard['name'],
            email=wizard['email'],
            phone=wizard['phone'],
            notes=wizard.get('notes', ''),
            status=Reservation.STATUS_CONFIRMED,
        )
        slot.is_booked = True
        slot.save(update_fields=['is_booked'])

        confirm_url = request.build_absolute_uri(
            reverse('reservations:confirm', kwargs={'token': reservation.confirmation_token})
        )
        send_mail(
            subject=_('Potvrzení rezervace — Black Velvet Spa'),
            message=_(
                'Dobrý den {name},\n\n'
                'Vaše rezervace byla potvrzena.\n'
                'Služba: {service}\n'
                'Termín: {date} {time}\n\n'
                'Potvrzení: {url}'
            ).format(
                name=reservation.name,
                service=service.name,
                date=slot.date,
                time=slot.time,
                url=confirm_url,
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.email],
            fail_silently=True,
        )

        _clear_wizard(request)
        return render(request, 'partials/htmx/reservation_success.html', {
            'reservation': reservation,
        })


class ReservationConfirmView(TemplateView):
    template_name = 'reservations/confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = kwargs.get('token')
        context['reservation'] = Reservation.objects.filter(confirmation_token=token).first()
        return context
