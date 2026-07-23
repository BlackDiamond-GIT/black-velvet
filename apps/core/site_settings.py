from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from .phone_rotation import (
    ROTATION_COUNT,
    active_index,
    format_tel_href,
    next_switch_at,
    normalize_whatsapp_digits,
    prague_now,
)


class SiteSettings(models.Model):
    phone_primary = models.CharField(_('Основний телефон'), max_length=30, default='+420 776 739 466')
    phone_secondary = models.CharField(_('Додатковий телефон'), max_length=30, blank=True)
    whatsapp_number = models.CharField(
        _('WhatsApp (без + і пробілів)'),
        max_length=20,
        default='420776739466',
        help_text=_('Напр. 420776739466 — для wa.me/'),
    )
    rotation_phone_1 = models.CharField(_('Ротаційний телефон 1'), max_length=30, default='+420 776 739 466')
    rotation_phone_2 = models.CharField(_('Ротаційний телефон 2'), max_length=30, default='+420 776 739 466')
    rotation_phone_3 = models.CharField(_('Ротаційний телефон 3'), max_length=30, default='+420 776 739 466')
    phone_rotation_hours = models.PositiveSmallIntegerField(_('Інтервал ротації (год)'), default=2)
    email = models.EmailField(_('Email'), default='info@black-velvet.cz')
    address = models.CharField(
        _('Адреса (студія 1)'),
        max_length=200,
        default='Lužická 1416/29, 120 00 Vinohrady',
    )
    location_phone_1 = models.CharField(_('Телефон (студія 1)'), max_length=30, default='+420 776 739 466')
    map_url = models.URLField(_('Посилання на карту (студія 1)'), max_length=500, blank=True)
    maps_embed_url = models.TextField(_('Google Maps embed URL (студія 1)'), blank=True)
    address_2 = models.CharField(_('Адреса (студія 2)'), max_length=200, blank=True)
    location_phone_2 = models.CharField(_('Телефон (студія 2)'), max_length=30, blank=True)
    map_url_2 = models.URLField(_('Посилання на карту (студія 2)'), max_length=500, blank=True)
    maps_embed_url_2 = models.TextField(_('Google Maps embed URL (студія 2)'), blank=True)
    hours = models.CharField(_('Години роботи (CS)'), max_length=100, default='Denně od 9:00 do 5:00')
    hours_en = models.CharField(_('Години роботи (EN)'), max_length=100, blank=True, default='Daily from 9 AM to 5 AM')
    hours_ru = models.CharField(_('Години роботи (RU)'), max_length=100, blank=True, default='Ежедневно с 9:00 до 5:00')
    instagram_url = models.URLField(_('Instagram'), blank=True)
    facebook_url = models.URLField(_('Facebook'), blank=True)
    whatsapp_url = models.URLField(_('WhatsApp URL'), blank=True, default='https://wa.me/420776739466')
    telegram_url = models.URLField(_('Telegram'), blank=True)
    default_meta_title = models.CharField(_('Meta title за замовчуванням'), max_length=200, blank=True)
    default_meta_description = models.CharField(_('Meta description за замовчуванням'), max_length=300, blank=True)
    og_image_url = models.URLField(_('OG image URL'), blank=True)
    require_age_confirmation = models.BooleanField(_('Підтвердження 18+'), default=True)

    class Meta:
        verbose_name = _('Налаштування сайту')
        verbose_name_plural = _('Налаштування сайту')

    def __str__(self):
        return str(_('Налаштування сайту'))

    def clean(self):
        super().clean()
        phones = self.get_rotation_phones()
        if not all(phones):
            raise ValidationError(_('Усі три ротаційні номери обовʼязкові.'))
        if self.phone_rotation_hours < 1:
            raise ValidationError({'phone_rotation_hours': _('Інтервал — мінімум 1 година.')})

    def save(self, *args, **kwargs):
        self.pk = 1
        for field in ('rotation_phone_1', 'rotation_phone_2', 'rotation_phone_3'):
            val = getattr(self, field, '') or ''
            setattr(self, field, val.strip())
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @classmethod
    def get(cls):
        return cls.load()

    def get_rotation_phones(self):
        return [
            (self.rotation_phone_1 or '').strip(),
            (self.rotation_phone_2 or '').strip(),
            (self.rotation_phone_3 or '').strip(),
        ]

    def get_active_phone_index(self, now=None):
        return active_index(now, interval_hours=self.phone_rotation_hours)

    def get_active_phone_display(self, now=None):
        phones = self.get_rotation_phones()
        if not all(phones):
            return (self.phone_primary or '').strip()
        return phones[self.get_active_phone_index(now)]

    def get_active_phone_tel(self, now=None):
        return format_tel_href(self.get_active_phone_display(now))

    def get_active_whatsapp_number(self, now=None):
        display = self.get_active_phone_display(now)
        digits = normalize_whatsapp_digits(display)
        if digits:
            return digits
        return normalize_whatsapp_digits(self.whatsapp_number)

    def get_rotation_preview(self, now=None):
        local = prague_now(now)
        switch = next_switch_at(now, interval_hours=self.phone_rotation_hours)
        idx = self.get_active_phone_index(now)
        return {
            'active': self.get_active_phone_display(now),
            'slot': idx + 1,
            'total': ROTATION_COUNT,
            'next_switch': switch.strftime('%H:%M'),
            'prague_now': local.strftime('%Y-%m-%d %H:%M'),
        }

    def get_hours_for_language(self, language_code):
        code = (language_code or 'cs').split('-')[0].lower()
        if code == 'en':
            text = (self.hours_en or '').strip()
            return text if text else self.hours
        if code == 'ru':
            text = (self.hours_ru or '').strip()
            return text if text else self.hours
        return self.hours

    def get_studio_locations(self, language_code=None):
        locations = []
        for address, map_url, phone in (
            (self.address, self.map_url, self.location_phone_1),
            (self.address_2, self.map_url_2, self.location_phone_2),
        ):
            addr = (address or '').strip()
            if not addr:
                continue
            phone_display = (phone or '').strip()
            locations.append({
                'address': addr,
                'map_url': (map_url or '').strip(),
                'phone_display': phone_display,
                'phone_tel': format_tel_href(phone_display) if phone_display else '',
            })
        return locations
