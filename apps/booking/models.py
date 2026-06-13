"""Booking models: WhatsApp message templates."""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


class WhatsAppTemplate(models.Model):
    """Editable pre-filled WhatsApp message templates per service."""

    SERVICE_CHOICES = [
        ("general", _("General / No service")),
        ("nuru", _("Nuru")),
        ("lingam", _("Lingam")),
        ("body", _("Body-to-Body")),
        ("bdsm", _("BDSM")),
        ("vip", _("VIP")),
        ("couple", _("Couples")),
        ("classic", _("Classic Erotic")),
        ("pussycat", _("Pussycat")),
        ("prostate", _("Prostate")),
    ]

    service_key = models.CharField(
        _("Service key"),
        max_length=30,
        choices=SERVICE_CHOICES,
        unique=True,
        default="general",
    )
    template_cs = models.TextField(
        _("Message template (CS)"),
        help_text=_("Use {masseuse} and {duration} placeholders."),
    )
    template_en = models.TextField(_("Message template (EN)"), blank=True)
    template_ru = models.TextField(_("Message template (RU)"), blank=True)

    class Meta:
        verbose_name = _("WhatsApp Template")
        verbose_name_plural = _("WhatsApp Templates")

    def __str__(self) -> str:
        return self.get_service_key_display()

    def get_message(self, lang: str = "cs", **kwargs: str) -> str:
        """Return formatted message in requested language."""
        m = {"cs": "template_cs", "en": "template_en", "ru": "template_ru"}
        template = getattr(self, m.get(lang, "template_cs"), "") or self.template_cs
        return template.format(**kwargs)


class BookingClick(models.Model):
    """One server-side hit on a booking redirect (WhatsApp or reservation)."""

    clicked_at = models.DateTimeField(_("Clicked at"), auto_now_add=True, db_index=True)
    channel = models.CharField(_("Channel"), max_length=16, db_index=True)
    placement = models.CharField(_("Placement"), max_length=40, db_index=True)
    page_path = models.CharField(_("Page path"), max_length=300, blank=True)
    lang = models.CharField(_("Language"), max_length=5, blank=True)
    masseuse_slug = models.CharField(_("Masseuse slug"), max_length=100, blank=True)
    service_slug = models.CharField(_("Service slug"), max_length=100, blank=True)
    duration_min = models.PositiveSmallIntegerField(_("Duration (min)"), null=True, blank=True)
    ip_hash = models.CharField(_("IP hash"), max_length=64, blank=True)
    ip_only_hash = models.CharField(_("IP-only hash"), max_length=64, blank=True, db_index=True)
    is_bot = models.BooleanField(_("Bot traffic"), default=False, db_index=True)

    class Meta:
        verbose_name = _("Booking click")
        verbose_name_plural = _("Booking clicks")
        ordering = ("-clicked_at",)
        indexes = [
            models.Index(fields=["clicked_at", "placement"]),
        ]

    def __str__(self) -> str:
        return f"{self.placement} ({self.channel}) @ {self.clicked_at:%Y-%m-%d %H:%M}"
