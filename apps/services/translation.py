from modeltranslation.translator import TranslationOptions, translator

from .models import Service


class ServiceTranslationOptions(TranslationOptions):
    fields = ('name', 'short_desc', 'description', 'meta_title', 'meta_description')


translator.register(Service, ServiceTranslationOptions)
