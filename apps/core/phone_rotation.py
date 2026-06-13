"""Phone rotation helpers (Europe/Prague wall clock)."""

from __future__ import annotations

import re
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

PRAGUE_TZ = ZoneInfo("Europe/Prague")
ROTATION_COUNT = 3


def prague_now(now: datetime | None = None) -> datetime:
    """Return aware datetime in Europe/Prague."""
    if now is None:
        from django.utils import timezone

        now = timezone.now()
    if now.tzinfo is None:
        from django.utils import timezone

        now = timezone.make_aware(now)
    return now.astimezone(PRAGUE_TZ)


def rotation_slot(hour: int, interval_hours: int, count: int = ROTATION_COUNT) -> int:
    """Map Prague hour to rotation index 0..count-1."""
    interval = max(1, interval_hours)
    return (hour // interval) % count


def active_index(
    now: datetime | None = None,
    *,
    interval_hours: int = 2,
    count: int = ROTATION_COUNT,
) -> int:
    """Current rotation slot for `now` (defaults to Django timezone.now())."""
    local = prague_now(now)
    return rotation_slot(local.hour, interval_hours, count)


def next_switch_at(
    now: datetime | None = None,
    *,
    interval_hours: int = 2,
) -> datetime:
    """Next slot boundary in Europe/Prague (aware)."""
    local = prague_now(now)
    interval = max(1, interval_hours)
    slot_start_hour = (local.hour // interval) * interval
    next_hour = slot_start_hour + interval
    base = local.replace(minute=0, second=0, microsecond=0)
    if next_hour >= 24:
        return (base + timedelta(days=1)).replace(hour=0)
    return base.replace(hour=next_hour)


def normalize_whatsapp_digits(phone: str) -> str:
    """Strip non-digits for wa.me/ links."""
    return re.sub(r"\D", "", phone or "")


def format_tel_href(phone: str) -> str:
    """E.164-style tel: href."""
    digits = normalize_whatsapp_digits(phone)
    if not digits:
        return ""
    return f"tel:+{digits}"
