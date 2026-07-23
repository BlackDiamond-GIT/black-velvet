from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import get_language

from apps.pages.currency import format_price


class Service(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    short_desc = models.CharField(max_length=300)
    description = models.TextField()
    duration_min = models.PositiveIntegerField(default=60)
    duration_max = models.PositiveIntegerField(default=90)
    price_czk = models.PositiveIntegerField()
    price_eur = models.PositiveIntegerField(default=0)
    price_usd = models.PositiveIntegerField(default=0)
    price_label = models.CharField(max_length=50, blank=True, help_text='e.g. od 500 Kč')
    image = models.ImageField(upload_to='services/', blank=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        if not self.price_label:
            self.price_label = f'od {self.price_czk} Kč'
        super().save(*args, **kwargs)

    def get_price_amount(self, currency='czk'):
        currency = (currency or 'czk').lower()
        if currency == 'eur':
            return self.price_eur
        if currency == 'usd':
            return self.price_usd
        return self.price_czk

    def formatted_price(self, currency='czk'):
        return format_price(self.get_price_amount(currency), currency)

    @property
    def localized_price_label(self):
        label = (self.price_label or f'od {self.price_czk} Kč').strip()
        if not label.lower().startswith('od '):
            return label

        prefix = {
            'cs': 'od',
            'en': 'from',
            'ru': 'от',
        }.get((get_language() or 'cs')[:2], 'od')
        return f'{prefix} {label[3:]}'

    def get_absolute_url(self):
        return reverse('services:detail', kwargs={'slug': self.slug})

    @property
    def duration_display(self):
        if self.duration_min == self.duration_max:
            return f'{self.duration_min} min'
        return f'{self.duration_min}–{self.duration_max} min'
