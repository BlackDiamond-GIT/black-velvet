from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.core.admin_forms import rich_text_widgets
from apps.core.admin_mixins import ImagePreviewMixin
from apps.core.velvet_admin import VelvetModelAdmin

from .models import Service


@admin.register(Service)
class ServiceAdmin(ImagePreviewMixin, VelvetModelAdmin, TabbedTranslationAdmin):
    list_display = ('name', 'get_image_preview', 'price_czk', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'short_desc')
    readonly_fields = ('get_image_preview', 'updated_at')
    fieldsets = (
        ('Основне', {
            'fields': ('name', 'slug', 'short_desc', 'description', 'image', 'get_image_preview'),
        }),
        ('Ціна та тривалість', {
            'fields': ('duration_min', 'duration_max', 'price_czk', 'price_eur', 'price_usd', 'price_label'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
        ('Статус', {
            'fields': ('is_active', 'order', 'updated_at'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        kwargs.setdefault('widgets', {})
        kwargs['widgets'].update(rich_text_widgets('description'))
        return super().get_form(request, obj, **kwargs)
