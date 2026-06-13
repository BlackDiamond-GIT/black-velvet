from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html


class ImagePreviewMixin:
    image_field = 'image'
    preview_height = 80

    @admin.display(description='Náhled')
    def get_image_preview(self, obj):
        image = getattr(obj, self.image_field, None)
        if image:
            return format_html(
                '<img src="{}" alt="" style="max-height:{}px;border-radius:4px;" />',
                image.url,
                self.preview_height,
            )
        return '—'


class SingletonAdminMixin:
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = self.model.objects.first()
        info = self.model._meta.app_label, self.model._meta.model_name
        if obj:
            return redirect(reverse(f'admin:{info[0]}_{info[1]}_change', args=[obj.pk]))
        return redirect(reverse(f'admin:{info[0]}_{info[1]}_add'))
