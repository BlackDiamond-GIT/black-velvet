from django.db import models


class SiteSettings(models.Model):
    instagram_url = models.URLField('Instagram', blank=True)
    facebook_url = models.URLField('Facebook', blank=True)
    whatsapp_url = models.URLField('WhatsApp', blank=True)

    class Meta:
        verbose_name = 'Nastavení webu'
        verbose_name_plural = 'Nastavení webu'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return 'Nastavení webu'
