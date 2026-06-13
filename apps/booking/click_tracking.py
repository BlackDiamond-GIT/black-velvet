"""Server-side booking click logging (WhatsApp + reservation redirects)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.core.cache import cache
from django.utils.translation import get_language

if TYPE_CHECKING:
    from django.http import HttpRequest

from .bot_detection import client_fingerprint, ip_only_hash_from_request, is_bot_click
from .models import BookingClick

# Whitelist — prevents garbage placement values in reports.
PLACEMENTS: frozenset[str] = frozenset(
    {
        "header_wa",
        "header_reservation",
        "footer_reservation",
        "footer_wa",
        "drawer_reservation",
        "mobile_nav_wa",
        "fab",
        "home_hero",
        "home_cta",
        "contact",
        "about",
        "prices",
        "jobs",
        "first_visit",
        "cms_contacts",
        "masseuse_card",
        "masseuse_detail_hero",
        "masseuse_detail_service",
        "masseuse_detail_sticky",
        "service_detail_intro",
        "service_detail_cta",
        "price_card",
        "schedule_row",
        "direct",
        "unknown",
    }
)

CHANNELS: frozenset[str] = frozenset({"whatsapp", "reservation"})

_DEDUP_SECONDS = 3
_CACHE_PREFIX = "booking_click_dedup:"


def normalize_placement(raw: str | None) -> str:
    value = (raw or "").strip().lower()[:40]
    if value in PLACEMENTS:
        return value
    return "unknown"


def _is_duplicate(fingerprint: str, placement: str) -> bool:
    key = f"{_CACHE_PREFIX}{fingerprint}:{placement}"
    if cache.get(key):
        return True
    cache.set(key, 1, timeout=_DEDUP_SECONDS)
    return False


def log_booking_click(
    request: HttpRequest,
    *,
    channel: str,
    placement: str,
    masseuse_slug: str = "",
    service_slug: str = "",
    duration_min: int | None = None,
) -> bool:
    """Persist one click. Returns False if deduplicated."""
    if channel not in CHANNELS:
        channel = "whatsapp"

    placement = normalize_placement(placement)
    fingerprint = client_fingerprint(request)
    if _is_duplicate(fingerprint, placement):
        return False

    ip_only_hash = ip_only_hash_from_request(request)

    lang = getattr(request, "LANGUAGE_CODE", None) or get_language() or "cs"
    referrer = (request.META.get("HTTP_REFERER") or "").strip()[:300]
    page_param = (request.GET.get("page") or "").strip()[:300]
    page_path = referrer or page_param or (request.path or "")[:300]

    BookingClick.objects.create(
        channel=channel,
        placement=placement,
        page_path=page_path,
        lang=lang.split("-")[0][:5],
        masseuse_slug=(masseuse_slug or "")[:100],
        service_slug=(service_slug or "")[:100],
        duration_min=duration_min,
        ip_hash=fingerprint[:64],
        ip_only_hash=ip_only_hash,
        is_bot=is_bot_click(request, ip_only_hash),
    )
    return True
