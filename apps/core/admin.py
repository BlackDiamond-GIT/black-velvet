from django.contrib import admin

from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Sociální sítě', {
            'fields': ('instagram_url', 'facebook_url', 'whatsapp_url'),
            'description': 'Odkazy na profily. Prázdné pole = zobrazena pouze ikona bez odkazu.',
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
