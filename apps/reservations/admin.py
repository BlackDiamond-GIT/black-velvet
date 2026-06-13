from django.contrib import admin

from apps.core.velvet_admin import VelvetModelAdmin

from .models import Reservation, TimeSlot


@admin.register(TimeSlot)
class TimeSlotAdmin(VelvetModelAdmin):
    list_display = ('date', 'time', 'masseuse', 'is_booked')
    list_filter = ('date', 'is_booked', 'masseuse')
    search_fields = ('masseuse__name',)
    date_hierarchy = 'date'


@admin.register(Reservation)
class ReservationAdmin(VelvetModelAdmin):
    list_display = ('name', 'service', 'masseuse', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'service', 'masseuse')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('confirmation_token', 'created_at')
    date_hierarchy = 'created_at'
