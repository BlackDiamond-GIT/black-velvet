from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import ContactMessage, FAQ, PriceCategory, PriceItem, Review


class PriceItemInline(admin.TabularInline):
    model = PriceItem
    extra = 1


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin):
    list_display = ('question', 'page', 'order', 'is_active')
    list_filter = ('page', 'is_active')


@admin.register(Review)
class ReviewAdmin(TranslationAdmin):
    list_display = ('author', 'rating', 'is_published', 'order')


@admin.register(PriceCategory)
class PriceCategoryAdmin(TranslationAdmin):
    inlines = [PriceItemInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'is_read')
    list_filter = ('is_read',)
