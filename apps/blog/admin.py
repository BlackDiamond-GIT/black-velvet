from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Post, Tag


@admin.register(Tag)
class TagAdmin(TranslationAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(TranslationAdmin):
    list_display = ('title', 'published_at', 'is_published')
    list_filter = ('is_published', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
