import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeSlot(models.Model):
    masseuse = models.ForeignKey(
        'team.Masseuse',
        on_delete=models.CASCADE,
        related_name='time_slots',
        null=True,
        blank=True,
        verbose_name=_('Masseuse'),
    )
    date = models.DateField(_('Date'))
    time = models.TimeField(_('Time'))
    is_booked = models.BooleanField(_('Booked'), default=False)

    class Meta:
        verbose_name = _('Schedule entry')
        verbose_name_plural = _('Schedule')
        ordering = ['date', 'time']
        unique_together = [('masseuse', 'date', 'time')]

    def __str__(self):
        return f'{self.date} {self.time}'


class Reservation(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_CONFIRMED, _('Confirmed')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]

    service = models.ForeignKey('services.Service', on_delete=models.PROTECT, verbose_name=_('Service'))
    masseuse = models.ForeignKey(
        'team.Masseuse',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Masseuse'),
    )
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, verbose_name=_('Time slot'))
    name = models.CharField(_('Name'), max_length=150)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Phone'), max_length=30)
    notes = models.TextField(_('Notes'), blank=True)
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.time_slot}'
