from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Masseuse


@admin.register(Masseuse)
class MasseuseAdmin(TranslationAdmin):
    list_display = ('name', 'years_experience', 'is_active', 'order')
    list_filter = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('services',)
