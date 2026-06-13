from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from unfold.admin import ModelAdmin, TabularInline

from apps.core.admin_forms import rich_text_widgets
from apps.core.velvet_admin import VelvetModelAdmin

from .models import ContactMessage, FAQ, PriceCategory, PriceItem, Review


class PriceItemInline(TabularInline):
    model = PriceItem
    extra = 1
    fields = ('service_name', 'duration', 'price', 'note', 'order')
    ordering = ('order',)


@admin.register(FAQ)
class FAQAdmin(VelvetModelAdmin, TabbedTranslationAdmin):
    list_display = ('question', 'page', 'order', 'is_active', 'include_in_schema')
    list_filter = ('page', 'is_active', 'include_in_schema')
    list_editable = ('order', 'is_active', 'include_in_schema')
    search_fields = ('question', 'answer')

    def get_form(self, request, obj=None, **kwargs):
        kwargs.setdefault('widgets', {})
        kwargs['widgets'].update(rich_text_widgets('answer'))
        return super().get_form(request, obj, **kwargs)


@admin.register(Review)
class ReviewAdmin(VelvetModelAdmin, TabbedTranslationAdmin):
    list_display = ('author', 'rating', 'is_published', 'order')
    list_filter = ('is_published', 'rating')
    list_editable = ('is_published', 'order')
    search_fields = ('author', 'text')

    def get_form(self, request, obj=None, **kwargs):
        kwargs.setdefault('widgets', {})
        kwargs['widgets'].update(rich_text_widgets('text'))
        return super().get_form(request, obj, **kwargs)


@admin.register(PriceCategory)
class PriceCategoryAdmin(VelvetModelAdmin, TabbedTranslationAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    inlines = [PriceItemInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(VelvetModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'phone', 'message')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
    list_editable = ('is_read',)

    def has_add_permission(self, request):
        return False
