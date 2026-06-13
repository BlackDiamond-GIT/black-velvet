from django.db import models


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
    note = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.service_name


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
