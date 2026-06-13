"""Admin for booking app."""

from __future__ import annotations

from django.contrib.admin.views.main import ERROR_FLAG
from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE

from apps.core.velvet_admin import VelvetModelAdmin

from .click_labels import channel_label, placement_label
from .click_stats import (
    build_click_dashboard,
    filter_queryset_by_audience,
    format_page_path,
    parse_audience,
)
from .models import BookingClick, WhatsAppTemplate


@admin.register(BookingClick)
class BookingClickAdmin(VelvetModelAdmin):
    list_display = (
        "clicked_at_local",
        "channel_display",
        "placement_display",
        "lang",
        "masseuse_slug",
        "page_display",
        "is_bot_display",
    )
    list_filter = ()  # custom filters in dashboard template
    date_hierarchy = "clicked_at"
    search_fields = ("placement", "masseuse_slug", "service_slug", "page_path")
    change_list_template = "admin/booking/bookingclick/change_list.html"
    readonly_fields = (
        "clicked_at",
        "channel",
        "placement",
        "page_path",
        "lang",
        "masseuse_slug",
        "service_slug",
        "duration_min",
        "ip_hash",
        "ip_only_hash",
        "is_bot",
    )

    @admin.display(description=_("Time (Prague)"), ordering="clicked_at")
    def clicked_at_local(self, obj: BookingClick) -> str:
        from django.utils import timezone

        return timezone.localtime(obj.clicked_at).strftime("%d.%m.%Y %H:%M")

    @admin.display(description=_("Channel"), ordering="channel")
    def channel_display(self, obj: BookingClick) -> str:
        return channel_label(obj.channel)

    @admin.display(description=_("Button"), ordering="placement")
    def placement_display(self, obj: BookingClick) -> str:
        return placement_label(obj.placement)

    @admin.display(description=_("Page"))
    def page_display(self, obj: BookingClick) -> str:
        return format_page_path(obj.page_path)

    @admin.display(description=_("Bot"), boolean=True, ordering="is_bot")
    def is_bot_display(self, obj: BookingClick) -> bool:
        return obj.is_bot

    # Dashboard-only GET params (days, chart, audience) are not model fields.
    # Django ChangeList treats unknown params as queryset filters → admin DB error page.
    _DASHBOARD_QUERY_KEYS = ("days", "chart", "audience", "date")

    def _audience_queryset(self, request: HttpRequest):
        audience = parse_audience(request.GET.get("audience"))
        return filter_queryset_by_audience(BookingClick.objects.all(), audience)

    def get_queryset(self, request: HttpRequest):
        qs = super().get_queryset(request)
        audience = parse_audience(request.GET.get("audience"))
        return filter_queryset_by_audience(qs, audience)

    def changelist_view(self, request: HttpRequest, extra_context=None):
        extra_context = extra_context or {}
        extra_context["click_dashboard"] = build_click_dashboard(
            self._audience_queryset(request),
            path=request.path,
            get_params=request.GET.dict(),
            source_queryset=BookingClick.objects.all(),
        )

        if any(key in request.GET for key in self._DASHBOARD_QUERY_KEYS):
            cleaned = request.GET.copy()
            for key in self._DASHBOARD_QUERY_KEYS:
                cleaned.pop(key, None)
            cleaned.pop(ERROR_FLAG, None)
            request.GET = cleaned

        return super().changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request: object) -> bool:
        return False

    def has_change_permission(self, request: object, obj: object | None = None) -> bool:
        return False

    def has_delete_permission(self, request: object, obj: object | None = None) -> bool:
        return request.user.is_superuser


@admin.register(WhatsAppTemplate)
class WhatsAppTemplateAdmin(VelvetModelAdmin):
    list_display = ("service_key", "template_cs")
    search_fields = ("service_key", "template_cs")

    formfield_overrides = {
        models.TextField: {"widget": TinyMCE},
    }

    fieldsets = (
        (None, {"fields": ("service_key",)}),
        (_("Template — Czech"), {"fields": ("template_cs",)}),
        (_("Template — English"), {"fields": ("template_en",)}),
        (_("Template — Russian"), {"fields": ("template_ru",)}),
    )
