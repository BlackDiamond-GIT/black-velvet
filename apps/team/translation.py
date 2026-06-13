from modeltranslation.translator import TranslationOptions, translator

from .models import Masseuse


class MasseuseTranslationOptions(TranslationOptions):
    fields = ('bio', 'specializations', 'meta_title', 'meta_description')


translator.register(Masseuse, MasseuseTranslationOptions)
