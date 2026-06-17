"""Sync schedule from tantra-prague.com Hub API into local MasseuseShift records.

Replaces the hardcoded WEEKLY_SHIFTS in schedule_data.py.

Strategy: fetch the next 14 days from the hub, extract weekday patterns,
then upsert MasseuseShift records. This gives the schedule.py DB-first
logic accurate recurring shift data without changing the display architecture.
"""

from __future__ import annotations

import datetime
from collections import defaultdict

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.hub_client.client import HubClient
from apps.hub_client.exceptions import HubUnavailableError
from apps.pages.models import MasseuseShift, WorkLocation
from apps.team.models import Masseuse


def _parse_time(value: str) -> datetime.time:
    h, m = map(int, value.split(':'))
    return datetime.time(h, m)


class Command(BaseCommand):
    help = "Sync schedule from tantra-prague.com Hub API → MasseuseShift patterns."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=14,
            help="Number of days to fetch for pattern extraction (default: 14)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview only — do not write to DB",
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]

        client = HubClient()
        try:
            raw_entries = client.fetch_schedule_json(days=days)
        except HubUnavailableError as exc:
            self.stderr.write(self.style.ERROR(f"Hub unreachable: {exc}"))
            return

        masseuse_by_slug = {
            m.slug: m for m in Masseuse.objects.filter(is_active=True)
        }
        default_location = WorkLocation.objects.filter(is_active=True).first()

        # Build weekday → shift patterns per masseuse slug
        # Key: (slug, weekday, time_from, time_to, period)
        patterns: dict[str, dict] = defaultdict(dict)

        for entry in raw_entries:
            slug = entry["masseuse_slug"]
            masseuse = masseuse_by_slug.get(slug)
            if not masseuse:
                continue

            entry_date = datetime.date.fromisoformat(entry["date"])
            weekday = entry_date.weekday()  # 0=Monday … 6=Sunday
            period = "night" if entry.get("shift_type") == "night" else "day"
            key = (slug, weekday, entry["time_from"], entry["time_to"], period)
            patterns[key] = {
                "masseuse": masseuse,
                "weekday": weekday,
                "start_time": _parse_time(entry["time_from"]),
                "end_time": _parse_time(entry["time_to"]),
                "period": period,
                "location": default_location,
            }

        if dry_run:
            self.stdout.write(f"[dry-run] Would upsert {len(patterns)} MasseuseShift records.")
            return

        created = updated = 0
        with transaction.atomic():
            # Mark existing synced shifts as inactive first (clean slate per masseuse)
            synced_slugs = {v["masseuse"].slug for v in patterns.values()}
            MasseuseShift.objects.filter(
                masseuse__slug__in=synced_slugs, is_active=True
            ).update(is_active=False)

            for data in patterns.values():
                obj, was_created = MasseuseShift.objects.update_or_create(
                    masseuse=data["masseuse"],
                    weekday=data["weekday"],
                    start_time=data["start_time"],
                    period=data["period"],     # include period in lookup to avoid day/night collision
                    defaults={
                        "end_time": data["end_time"],
                        "location": data["location"],
                        "is_active": True,
                        "order": data["weekday"],
                    },
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        self.stdout.write(
            f"Synced {len(raw_entries)} hub entries → "
            f"created {created}, updated {updated} MasseuseShift records."
        )
        self.stdout.write(self.style.SUCCESS("Schedule synced from hub API."))
