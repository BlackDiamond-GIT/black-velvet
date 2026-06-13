from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _


class Masseuse(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)
    bio = models.TextField()
    specializations = models.CharField(max_length=200)
    years_experience = models.PositiveIntegerField(default=1)
    photo = models.ImageField(upload_to='team/', blank=True)
    services = models.ManyToManyField('services.Service', blank=True, related_name='masseuses')
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Masseuse'
        verbose_name_plural = 'Masseuses'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('team:detail', kwargs={'slug': self.slug})

    @property
    def specializations_list(self):
        return [s.strip() for s in self.specializations.split(',') if s.strip()]

    @property
    def experience_display(self):
        years = self.years_experience
        if years == 1:
            return _('1 rok')
        if 2 <= years <= 4:
            return _('%s roky') % years
        return _('%s let') % years
