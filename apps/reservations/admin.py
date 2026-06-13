from django.contrib import admin

from .models import Reservation, TimeSlot


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'masseuse', 'is_booked')
    list_filter = ('date', 'is_booked')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'masseuse', 'time_slot', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('confirmation_token', 'created_at')
