"""Admin for CMS page content and interior gallery."""

from __future__ import annotations

from django.conf import settings
from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from apps.core.velvet_admin import VelvetModelAdmin

from apps.team.widgets import CloudinaryFKWidget

from .models import ContentPage, EtiquetteRule, GuestReview, InteriorImage

_PAGE_KEY_UK = {
    ContentPage.PageKey.PRIVACY: "Політика конфіденційності",
    ContentPage.PageKey.FIRST_VISIT: "Перший візит",
    ContentPage.PageKey.PRICES: "Ціни",
    ContentPage.PageKey.JOBS: "Вакансії",
}


@admin.register(ContentPage)
class ContentPageAdmin(VelvetModelAdmin):
    list_display = ("page_title", "updated_at")
    readonly_fields = ("page_key", "updated_at")
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE},
    }

    fieldsets = (
        (None, {"fields": ("page_key", "updated_at")}),
        (
            _("Czech"),
            {"fields": ("hero_sub_cs", "body_cs")},
        ),
        (
            _("English"),
            {"fields": ("hero_sub_en", "body_en")},
        ),
        (
            _("Russian"),
            {"fields": ("hero_sub_ru", "body_ru")},
        ),
    )

    def has_add_permission(self, request: object) -> bool:  # type: ignore[override]
        return ContentPage.objects.count() < len(ContentPage.PageKey.choices)

    def has_delete_permission(self, request: object, obj: object = None) -> bool:  # type: ignore[override]
        return False

    def get_fieldsets(self, request, obj=None):  # type: ignore[override]
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.page_key == ContentPage.PageKey.PRICES:
            return (
                fieldsets[0],
                (_("Czech"), {"fields": ("hero_sub_cs",)}),
                (_("English"), {"fields": ("hero_sub_en",)}),
                (_("Russian"), {"fields": ("hero_sub_ru",)}),
            )
        return fieldsets

    @admin.display(description=_("Page"), ordering="page_key")
    def page_title(self, obj: ContentPage) -> str:
        if get_language() == "uk":
            return _PAGE_KEY_UK.get(obj.page_key, obj.page_key)
        return obj.get_page_key_display()  # type: ignore[attr-defined]


@admin.register(InteriorImage)
class InteriorImageAdmin(VelvetModelAdmin):
    list_display = ("thumb_preview", "alt_cs", "sort_order", "is_active", "source_label")
    list_editable = ("sort_order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("alt_cs", "static_path", "cloudinary_image__title")
    readonly_fields = ("thumb_preview", "created_at")
    autocomplete_fields = ()

    def get_fieldsets(self, request, obj=None):  # type: ignore[override]
        fieldsets = [
            (None, {"fields": ("is_active", "sort_order", "thumb_preview")}),
            (
                _("Photos — Cloudinary Library"),
                {
                    "fields": ("cloudinary_image",),
                    "description": _(
                        "Upload the image in Media Library, then pick it here — "
                        "same workflow as masseuse photos."
                    ),
                },
            ),
            (_("Alt text"), {"fields": ("alt_cs", "alt_en", "alt_ru")}),
            (_("Meta"), {"fields": ("created_at",), "classes": ("collapse",)}),
        ]
        legacy_fields: list[str] = ["static_path"]
        if not settings.CLOUDINARY_URL:
            legacy_fields.insert(0, "image")
        fieldsets.insert(
            2,
            (
                _("Photos — Legacy (file / static path)"),
                {"fields": tuple(legacy_fields), "classes": ("collapse",)},
            ),
        )
        return fieldsets

    def get_form(self, request: object, obj: InteriorImage | None = None, **kwargs: object) -> type:
        form = super().get_form(request, obj, **kwargs)
        if "cloudinary_image" in form.base_fields:
            field = form.base_fields["cloudinary_image"]
            field.widget = CloudinaryFKWidget(choices=field.widget.choices)
            if get_language() == "uk":
                field.empty_label = "Оберіть значення"
        return form

    @admin.display(description=_("Preview"))
    def thumb_preview(self, obj: InteriorImage) -> str:
        url = obj.get_image_url()
        if url:
            return format_html(
                '<img src="{}" style="height:56px;width:84px;object-fit:cover;border-radius:4px">',
                url,
            )
        return "—"

    @admin.display(description=_("Source"))
    def source_label(self, obj: InteriorImage) -> str:
        if obj.cloudinary_image_id:
            return "Cloudinary"
        if obj.image:
            return _("Upload")
        if obj.static_path:
            return _("Static")
        return "—"


@admin.register(EtiquetteRule)
class EtiquetteRuleAdmin(VelvetModelAdmin):
    list_display = ("rule_preview", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active", "category")
    search_fields = ("rule_cs", "rule_en", "rule_ru")

    fieldsets = (
        (None, {"fields": ("is_active", "category", "order")}),
        (_("Czech"), {"fields": ("rule_cs",)}),
        (_("English"), {"fields": ("rule_en",)}),
        (_("Russian"), {"fields": ("rule_ru",)}),
    )

    @admin.display(description=_("Rule"), ordering="rule_cs")
    def rule_preview(self, obj: EtiquetteRule) -> str:
        return obj.rule_cs[:80]


@admin.register(GuestReview)
class GuestReviewAdmin(VelvetModelAdmin):
    list_display = ("author_label", "city", "order", "is_active", "text_preview")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("author_label", "city", "text_cs", "text_en", "text_ru")
    readonly_fields = ("created_at",)

    fieldsets = (
        (None, {"fields": ("is_active", "order", "author_label", "city", "rating")}),
        (_("Czech"), {"fields": ("text_cs",)}),
        (_("English"), {"fields": ("text_en",)}),
        (_("Russian"), {"fields": ("text_ru",)}),
        (
            _("Google"),
            {
                "fields": ("google_review_id",),
                "classes": ("collapse",),
            },
        ),
        (_("Meta"), {"fields": ("created_at",), "classes": ("collapse",)}),
    )

    @admin.display(description=_("Review"))
    def text_preview(self, obj: GuestReview) -> str:
        return obj.text_cs[:80]
