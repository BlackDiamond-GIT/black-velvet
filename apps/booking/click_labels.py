"""Human-readable labels for booking click admin."""

from __future__ import annotations

from django.utils.translation import gettext_lazy as _

PLACEMENT_LABELS: dict[str, str] = {
    "header_wa": _("WhatsApp in header"),
    "header_reservation": _("Reservation in header"),
    "footer_reservation": _("Reservation in footer"),
    "footer_wa": _("WhatsApp in footer"),
    "drawer_reservation": _("Reservation in menu"),
    "mobile_nav_wa": _("WhatsApp in mobile nav"),
    "fab": _("Floating WhatsApp button"),
    "home_hero": _("Home — hero button"),
    "home_cta": _("Home — bottom CTA"),
    "contact": _("Contact page"),
    "about": _("About page"),
    "prices": _("Price list page"),
    "jobs": _("Jobs page"),
    "first_visit": _("First visit page"),
    "cms_contacts": _("CMS contacts"),
    "masseuse_card": _("Masseuse card"),
    "masseuse_detail_hero": _("Masseuse page — main button"),
    "masseuse_detail_service": _("Masseuse page — service"),
    "masseuse_detail_sticky": _("Masseuse page — sticky bar"),
    "service_detail_intro": _("Service page — top"),
    "service_detail_cta": _("Service page — CTA"),
    "price_card": _("Price card button"),
    "schedule_row": _("Schedule row"),
    "direct": _("Direct /rezervace/ link"),
    "unknown": _("Other"),
}

CHANNEL_LABELS: dict[str, str] = {
    "whatsapp": _("WhatsApp button"),
    "reservation": _("Reservation link"),
}


def placement_label(key: str) -> str:
    return str(PLACEMENT_LABELS.get(key, PLACEMENT_LABELS["unknown"]))


def channel_label(key: str) -> str:
    return str(CHANNEL_LABELS.get(key, key))
