from modeltranslation.translator import TranslationOptions, translator

from .models import Post, Tag


class TagTranslationOptions(TranslationOptions):
    fields = ('name',)


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'excerpt', 'content', 'meta_title', 'meta_description')


translator.register(Tag, TagTranslationOptions)
translator.register(Post, PostTranslationOptions)
