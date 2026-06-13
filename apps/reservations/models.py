import uuid

from django.db import models


class TimeSlot(models.Model):
    masseuse = models.ForeignKey(
        'team.Masseuse',
        on_delete=models.CASCADE,
        related_name='time_slots',
        null=True,
        blank=True,
    )
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'time']
        unique_together = [('masseuse', 'date', 'time')]

    def __str__(self):
        return f'{self.date} {self.time}'


class Reservation(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_CONFIRMED, 'Confirmed'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]

    service = models.ForeignKey('services.Service', on_delete=models.PROTECT)
    masseuse = models.ForeignKey(
        'team.Masseuse',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.time_slot}'
