"""Retroactive bot reclassification for BookingClick records."""

from __future__ import annotations

import datetime
from collections import defaultdict
from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

from django.db.models import Count
from django.db.models.functions import TruncHour
from django.utils import timezone

from .bot_detection import DAILY_RATE_LIMIT, HOURLY_RATE_LIMIT

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from .models import BookingClick

PRAGUE_TZ = ZoneInfo("Europe/Prague")


@dataclass
class ReclassifyResult:
    marked_ids: set[int] = field(default_factory=set)
    hourly_ip_hash_ids: set[int] = field(default_factory=set)
    daily_ip_hash_ids: set[int] = field(default_factory=set)
    hourly_ip_only_ids: set[int] = field(default_factory=set)
    daily_ip_only_ids: set[int] = field(default_factory=set)

    @property
    def total_marked(self) -> int:
        return len(self.marked_ids)


def _collect_hourly_suspicious_ids(
    queryset: QuerySet[BookingClick],
    *,
    hash_field: str,
    threshold: int = HOURLY_RATE_LIMIT,
) -> set[int]:
    suspicious: set[int] = set()
    groups = (
        queryset.exclude(**{hash_field: ""})
        .annotate(hour=TruncHour("clicked_at"))
        .values(hash_field, "hour")
        .annotate(count=Count("id"))
        .filter(count__gte=threshold)
    )
    for row in groups:
        ids = queryset.filter(
            **{hash_field: row[hash_field]},
            clicked_at__gte=row["hour"],
            clicked_at__lt=row["hour"] + datetime.timedelta(hours=1),
        ).values_list("id", flat=True)
        suspicious.update(ids)
    return suspicious


def _collect_daily_suspicious_ids(
    queryset: QuerySet[BookingClick],
    *,
    hash_field: str,
    threshold: int = DAILY_RATE_LIMIT,
) -> set[int]:
    suspicious: set[int] = set()
    counts: dict[tuple[str, datetime.date], int] = defaultdict(int)
    id_map: dict[tuple[str, datetime.date], list[int]] = defaultdict(list)

    for pk, hash_value, clicked_at in queryset.exclude(**{hash_field: ""}).values_list(
        "id", hash_field, "clicked_at"
    ):
        day = clicked_at.astimezone(PRAGUE_TZ).date()
        key = (hash_value, day)
        counts[key] += 1
        id_map[key].append(pk)

    for _key, count in counts.items():
        if count >= threshold:
            suspicious.update(id_map[_key])
    return suspicious


def find_suspicious_click_ids(
    queryset: QuerySet[BookingClick],
) -> ReclassifyResult:
    """Find click IDs that exceed hourly/daily rate thresholds."""
    result = ReclassifyResult()

    result.hourly_ip_hash_ids = _collect_hourly_suspicious_ids(queryset, hash_field="ip_hash")
    result.marked_ids.update(result.hourly_ip_hash_ids)

    result.daily_ip_hash_ids = _collect_daily_suspicious_ids(queryset, hash_field="ip_hash")
    result.marked_ids.update(result.daily_ip_hash_ids)

    result.hourly_ip_only_ids = _collect_hourly_suspicious_ids(queryset, hash_field="ip_only_hash")
    result.marked_ids.update(result.hourly_ip_only_ids)

    result.daily_ip_only_ids = _collect_daily_suspicious_ids(queryset, hash_field="ip_only_hash")
    result.marked_ids.update(result.daily_ip_only_ids)

    return result


def apply_reclassification(
    queryset: QuerySet[BookingClick],
    *,
    dry_run: bool = True,
) -> ReclassifyResult:
    """Mark suspicious clicks as bots. Returns stats (dry_run skips DB write)."""
    result = find_suspicious_click_ids(queryset)
    if not dry_run and result.marked_ids:
        queryset.model.objects.filter(pk__in=result.marked_ids, is_bot=False).update(is_bot=True)
    return result


def day_queryset(queryset: QuerySet[BookingClick], day: datetime.date) -> QuerySet[BookingClick]:
    """Filter queryset to one Prague calendar day."""
    start = timezone.make_aware(
        datetime.datetime.combine(day, datetime.time.min),
        PRAGUE_TZ,
    )
    end = start + datetime.timedelta(days=1)
    return queryset.filter(clicked_at__gte=start, clicked_at__lt=end)


def top_noisy_fingerprints(
    queryset: QuerySet[BookingClick],
    *,
    limit: int = 5,
) -> list[tuple[str, int]]:
    """Return top ip_hash values by click count."""
    rows = (
        queryset.exclude(ip_hash="")
        .values("ip_hash")
        .annotate(count=Count("id"))
        .order_by("-count")[:limit]
    )
    return [(row["ip_hash"][:12] + "…", row["count"]) for row in rows]
