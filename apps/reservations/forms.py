from datetime import date, timedelta

from django import forms
from django.utils.translation import gettext_lazy as _

from apps.services.models import Service
from apps.team.models import Masseuse

from .models import Reservation, TimeSlot


class Step1ServiceForm(forms.Form):
    service = forms.ModelChoiceField(
        queryset=Service.objects.filter(is_active=True),
        widget=forms.RadioSelect,
        label=_('Vyberte masáž'),
    )


class Step2MasseuseForm(forms.Form):
    masseuse = forms.ModelChoiceField(
        queryset=Masseuse.objects.filter(is_active=True),
        required=False,
        widget=forms.RadioSelect,
        label=_('Vyberte masérku'),
        empty_label=_('Libovolná masérka'),
    )


class Step3DateTimeForm(forms.Form):
    slot_date = forms.DateField(
        label=_('Datum'),
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
    )
    slot_time = forms.TimeField(
        label=_('Čas'),
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
    )

    def __init__(self, *args, masseuse=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.masseuse = masseuse

    def clean(self):
        cleaned = super().clean()
        slot_date = cleaned.get('slot_date')
        slot_time = cleaned.get('slot_time')
        if slot_date and slot_time:
            if slot_date < date.today():
                raise forms.ValidationError(_('Datum musí být v budoucnosti.'))
            qs = TimeSlot.objects.filter(date=slot_date, time=slot_time, is_booked=False)
            if self.masseuse:
                qs = qs.filter(masseuse=self.masseuse)
            if not qs.exists():
                slot, _ = TimeSlot.objects.get_or_create(
                    masseuse=self.masseuse,
                    date=slot_date,
                    time=slot_time,
                    defaults={'is_booked': False},
                )
                cleaned['time_slot'] = slot
            else:
                cleaned['time_slot'] = qs.first()
        return cleaned


class Step4ContactForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['name', 'email', 'phone', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('Jméno a příjmení')}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': _('Email')}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': _('Telefon')}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'placeholder': _('Poznámka (volitelné)'), 'rows': 3}),
        }


def get_available_dates(masseuse=None, days=14):
    today = date.today()
    return [today + timedelta(days=i) for i in range(days)]


def get_available_times():
    return ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']
