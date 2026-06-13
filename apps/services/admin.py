from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Service


@admin.register(Service)
class ServiceAdmin(TranslationAdmin):
    list_display = ('name', 'price_czk', 'is_active', 'order')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
