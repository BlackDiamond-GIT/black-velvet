"""Admin for Media Library — Cloudinary image uploads and management."""

from __future__ import annotations

import os

from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.utils.translation import gettext_lazy as _
from apps.core.velvet_admin import VelvetModelAdmin

from .models import CloudinaryImage


@admin.register(CloudinaryImage)
class CloudinaryImageAdmin(VelvetModelAdmin):
    list_display = (
        "thumb_preview",
        "title",
        "public_id",
        "format",
        "dimensions",
        "masseuse_assignment",
        "assign_btn",
        "uploaded_at",
    )
    list_display_links = ("thumb_preview", "title")
    search_fields = ("title", "public_id")
    list_filter = ("format",)
    readonly_fields = (
        "public_id",
        "secure_url",
        "width",
        "height",
        "format",
        "bytes",
        "uploaded_at",
        "large_preview",
    )
    fields = (
        "large_preview",
        "title",
        "public_id",
        "secure_url",
        "width",
        "height",
        "format",
        "bytes",
        "uploaded_at",
    )

    change_list_template = "admin/media_library/cloudinaryimage/change_list.html"

    def get_cloudinary_config(self):
        return {
            "cloud_name": os.getenv("CLOUDINARY_CLOUD_NAME", ""),
            "api_key": os.getenv("CLOUDINARY_API_KEY", ""),
            "configured": bool(os.getenv("CLOUDINARY_URL", "")),
        }

    def changelist_view(self, request, extra_context=None):
        from apps.team.models import Masseuse

        extra_context = extra_context or {}
        extra_context["cloudinary_config"] = self.get_cloudinary_config()
        extra_context["masseuses_list"] = list(
            Masseuse.objects.order_by('order', 'name').values('id', 'name')
        )
        return super().changelist_view(request, extra_context=extra_context)

    @admin.display(description=_("Assigned to"))
    def masseuse_assignment(self, obj: CloudinaryImage) -> str:
        parts = []
        for m in obj.masseuse_main.all():
            parts.append(
                format_html(
                    '<span style="display:inline-block;background:#4f46e5;color:#fff;'
                    'font-size:0.7rem;padding:1px 6px;border-radius:3px;margin:1px">'
                    "{} — {}</span>",
                    m.name,
                    _("main"),
                )
            )
        for m in obj.masseuse_gallery.all():
            parts.append(
                format_html(
                    '<span style="display:inline-block;background:#0e7490;color:#fff;'
                    'font-size:0.7rem;padding:1px 6px;border-radius:3px;margin:1px">'
                    "{} — {}</span>",
                    m.name,
                    _("gallery"),
                )
            )
        if not parts:
            return mark_safe('<span style="color:#6b7280">—</span>')
        return mark_safe("".join(parts))

    @admin.display(description="")
    def assign_btn(self, obj: CloudinaryImage) -> str:
        import json as _json

        assignments = []
        for m in obj.masseuse_main.all():
            assignments.append({"masseuse_id": m.pk, "masseuse_name": m.name, "type": "main"})
        for m in obj.masseuse_gallery.all():
            assignments.append({"masseuse_id": m.pk, "masseuse_name": m.name, "type": "gallery"})

        return format_html(
            '<button type="button" class="cld-assign-btn" data-image-id="{}" data-assignments="{}" '
            'style="cursor:pointer;background:#4f46e5;color:#fff;border:none;'
            'padding:4px 10px;border-radius:4px;font-size:0.78rem;white-space:nowrap">'
            "{}</button>",
            obj.pk,
            _json.dumps(assignments).replace('"', "&quot;"),
            _("Assign"),
        )

    @admin.display(description=_("Preview"))
    def thumb_preview(self, obj: CloudinaryImage) -> str:
        if not obj.secure_url:
            return "—"
        return format_html(
            '<img src="{}" style="height:56px;width:56px;object-fit:cover;border-radius:4px">',
            obj.thumbnail_url,
        )

    @admin.display(description=_("Full preview"))
    def large_preview(self, obj: CloudinaryImage) -> str:
        if not obj.secure_url:
            return "—"
        return format_html(
            '<img src="{}" style="max-height:300px;max-width:100%;border-radius:6px">',
            obj.display_url,
        )

    @admin.display(description=_("Dimensions"))
    def dimensions(self, obj: CloudinaryImage) -> str:
        if obj.width and obj.height:
            return f"{obj.width}×{obj.height}"
        return "—"
