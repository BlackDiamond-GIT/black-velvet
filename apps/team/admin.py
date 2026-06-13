from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from modeltranslation.admin import TabbedTranslationAdmin

from apps.core.admin_forms import rich_text_widgets
from apps.core.velvet_admin import VelvetModelAdmin
from apps.team.widgets import CloudinaryFKWidget, CloudinaryM2MWidget

from .models import Masseuse


@admin.register(Masseuse)
class MasseuseAdmin(VelvetModelAdmin, TabbedTranslationAdmin):
    list_display = (
        'photo_preview',
        'name',
        'age',
        'years_experience',
        'is_active',
        'is_busy',
        'has_location',
        'col_schedule',
        'col_new',
        'order',
    )
    list_filter = ('is_active', 'is_busy', 'has_location', 'is_new')
    list_editable = ('is_active', 'is_busy', 'has_location', 'order')
    search_fields = ('name', 'slug', 'specializations')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('services', 'gallery_cloudinary')
    readonly_fields = ('photo_preview', 'updated_at')

    fieldsets = (
        (_('Профіль'), {
            'fields': ('name', 'slug', 'order', 'is_active', 'is_new'),
        }),
        (_('Статус'), {
            'fields': ('is_busy', 'has_location', 'has_schedule'),
        }),
        (_('Фізичні дані'), {
            'fields': ('age', 'height_cm', 'weight_kg', 'bust', 'years_experience'),
        }),
        (_('Фото — бібліотека Cloudinary'), {
            'fields': ('photo_preview', 'main_cloudinary_photo', 'gallery_cloudinary'),
        }),
        (_('Фото — локальний файл'), {
            'fields': ('photo',),
            'classes': ('collapse',),
        }),
        (_('Контент'), {
            'fields': ('specializations', 'bio'),
        }),
        (_('Послуги'), {
            'fields': ('services',),
        }),
        (_('SEO'), {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
        (_('Системне'), {
            'fields': ('updated_at',),
            'classes': ('collapse',),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        kwargs.setdefault('widgets', {})
        kwargs['widgets'].update(rich_text_widgets('bio'))
        form = super().get_form(request, obj, **kwargs)
        if 'main_cloudinary_photo' in form.base_fields:
            form.base_fields['main_cloudinary_photo'].widget = CloudinaryFKWidget(
                choices=form.base_fields['main_cloudinary_photo'].widget.choices,
            )
        if 'gallery_cloudinary' in form.base_fields:
            form.base_fields['gallery_cloudinary'].widget = CloudinaryM2MWidget(
                choices=form.base_fields['gallery_cloudinary'].widget.choices,
            )
        return form

    @admin.display(description=_('Фото'))
    def photo_preview(self, obj):
        url = obj.photo_url
        if url:
            return format_html(
                '<img src="{}" style="height:60px;width:48px;object-fit:cover;border-radius:4px">',
                url,
            )
        return '—'

    @admin.display(description=_('Розкл.'), boolean=True)
    def col_schedule(self, obj):
        return obj.has_schedule

    @admin.display(description=_('Нова'), boolean=True)
    def col_new(self, obj):
        return obj.is_new
