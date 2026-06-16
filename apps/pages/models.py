from django.db import models

from .currency import format_price


class FAQ(models.Model):
    PAGE_HOME = 'home'
    PAGE_SERVICE = 'service'
    PAGE_GENERAL = 'general'
    PAGE_CHOICES = [
        (PAGE_HOME, 'Home'),
        (PAGE_SERVICE, 'Service'),
        (PAGE_GENERAL, 'General'),
    ]

    question = models.CharField(max_length=300)
    answer = models.TextField()
    page = models.CharField(max_length=20, choices=PAGE_CHOICES, default=PAGE_GENERAL)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    include_in_schema = models.BooleanField('У schema.org', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class Review(models.Model):
    author = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.author


class PriceCategory(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Price categories'

    def __str__(self):
        return self.name


class PriceItem(models.Model):
    category = models.ForeignKey(PriceCategory, on_delete=models.CASCADE, related_name='items')
    service_name = models.CharField(max_length=150)
    duration = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    price_czk = models.PositiveIntegerField(default=0)
    price_eur = models.PositiveIntegerField(default=0)
    price_usd = models.PositiveIntegerField(default=0)
    note = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.service_name

    def save(self, *args, **kwargs):
        if self.price_czk and not self.price:
            self.price = format_price(self.price_czk, 'czk')
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


class WorkLocation(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Work location'
        verbose_name_plural = 'Work locations'

    def __str__(self):
        return self.name or self.address


class MasseuseShift(models.Model):
    PERIOD_DAY = 'day'
    PERIOD_NIGHT = 'night'
    PERIOD_CHOICES = [
        (PERIOD_DAY, 'Day'),
        (PERIOD_NIGHT, 'Night'),
    ]

    masseuse = models.ForeignKey(
        'team.Masseuse',
        on_delete=models.CASCADE,
        related_name='shifts',
    )
    weekday = models.PositiveSmallIntegerField(
        help_text='0 = Monday … 6 = Sunday',
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default=PERIOD_DAY)
    location = models.ForeignKey(
        WorkLocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shifts',
    )
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['weekday', 'order', 'start_time']
        verbose_name = 'Masseuse shift'
        verbose_name_plural = 'Masseuse shifts'

    def __str__(self):
        return f'{self.masseuse} — {self.weekday} {self.start_time:%H:%M}–{self.end_time:%H:%M}'


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.created_at:%Y-%m-%d}'
