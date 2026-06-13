"""WhatsApp URL builder utility."""

from __future__ import annotations

import urllib.parse

from django.utils.translation import get_language

from apps.core.models import SiteSettings


def build_whatsapp_url(
    masseuse_name: str = "",
    service_name: str = "",
    duration: str = "",
    lang: str | None = None,
) -> str:
    """Build wa.me URL with pre-filled booking message."""
    settings = SiteSettings.get()
    number = settings.get_active_whatsapp_number()

    if not lang:
        lang = get_language() or "cs"

    # Build message
    parts = []
    if masseuse_name:
        parts.append(f"Masseuse: {masseuse_name}")
    if service_name:
        parts.append(f"Service: {service_name}")
    if duration:
        parts.append(f"Duration: {duration} min")

    message = "Hello, I would like to book:\n" + "\n".join(parts) if parts else ""

    if lang == "cs":
        message = "Dobrý den, rád/a bych zarezervoval/a:\n" + "\n".join(parts) if parts else ""
    elif lang == "ru":
        message = "Здравствуйте, хочу записаться:\n" + "\n".join(parts) if parts else ""

    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{number}?text={encoded}"
