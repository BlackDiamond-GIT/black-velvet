"""Admin for CMS page content."""

from __future__ import annotations

from django.contrib import admin
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE
from apps.core.velvet_admin import VelvetModelAdmin

from .models import ContentPage, GuestReview

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
