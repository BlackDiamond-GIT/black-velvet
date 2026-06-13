from modeltranslation.translator import TranslationOptions, translator

from .models import FAQ, PriceCategory, PriceItem, Review


class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')


class ReviewTranslationOptions(TranslationOptions):
    fields = ('role', 'text')


class PriceCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class PriceItemTranslationOptions(TranslationOptions):
    fields = ('service_name', 'note')


translator.register(FAQ, FAQTranslationOptions)
translator.register(Review, ReviewTranslationOptions)
translator.register(PriceCategory, PriceCategoryTranslationOptions)
translator.register(PriceItem, PriceItemTranslationOptions)
