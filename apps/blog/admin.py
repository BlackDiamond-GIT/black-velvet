from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from apps.core.admin_forms import rich_text_widgets
from apps.core.admin_mixins import ImagePreviewMixin
from apps.core.velvet_admin import VelvetModelAdmin

from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(VelvetModelAdmin, TabbedTranslationAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(ImagePreviewMixin, VelvetModelAdmin, TabbedTranslationAdmin):
    list_display = ('title', 'get_image_preview', 'published_at', 'is_published')
    list_filter = ('is_published', 'tags', 'published_at')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'excerpt', 'content')
    readonly_fields = ('get_image_preview', 'updated_at')
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Контент', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'image', 'get_image_preview', 'tags'),
        }),
        ('Автор і публікація', {
            'fields': ('author_name', 'author', 'published_at', 'is_published', 'updated_at'),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        kwargs.setdefault('widgets', {})
        kwargs['widgets'].update(rich_text_widgets('content', 'excerpt'))
        return super().get_form(request, obj, **kwargs)
