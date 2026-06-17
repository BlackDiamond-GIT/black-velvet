"""Sync schedule from tantra-prague.com Hub API into local MasseuseShift records.

Falls back to WEEKLY_SHIFTS in schedule_data.py when the hub is unreachable
or HUB_API_KEY is not configured (cron stays green on Render).
"""

from __future__ import annotations

import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.hub_client.client import HubClient
from apps.hub_client.exceptions import HubAPIError, HubUnavailableError
from apps.pages.models import MasseuseShift, WorkLocation
from apps.pages.schedule_data import WEEKLY_SHIFTS
from apps.team.models import Masseuse


def _parse_time(value: str) -> datetime.time:
    hour, minute = map(int, value.split(':'))
    return datetime.time(hour, minute)


def _patterns_from_hub(raw_entries, masseuse_by_slug, default_location):
    patterns = {}
    for entry in raw_entries:
        slug = entry["masseuse_slug"]
        masseuse = masseuse_by_slug.get(slug)
        if not masseuse:
            continue

        entry_date = datetime.date.fromisoformat(entry["date"])
        weekday = entry_date.weekday()
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
    return patterns


def _patterns_from_weekly_shifts(masseuse_by_slug, default_location):
    patterns = {}
    for slug, days in WEEKLY_SHIFTS.items():
        masseuse = masseuse_by_slug.get(slug)
        if not masseuse:
            continue
        for weekday, shifts in days.items():
            for shift in shifts:
                key = (slug, weekday, shift["start"], shift["end"], shift["period"])
                patterns[key] = {
                    "masseuse": masseuse,
                    "weekday": weekday,
                    "start_time": _parse_time(shift["start"]),
                    "end_time": _parse_time(shift["end"]),
                    "period": shift["period"],
                    "location": default_location,
                }
    return patterns


def _upsert_patterns(patterns):
    created = updated = 0
    with transaction.atomic():
        synced_slugs = {data["masseuse"].slug for data in patterns.values()}
        MasseuseShift.objects.filter(
            masseuse__slug__in=synced_slugs, is_active=True
        ).update(is_active=False)

        for data in patterns.values():
            _, was_created = MasseuseShift.objects.update_or_create(
                masseuse=data["masseuse"],
                weekday=data["weekday"],
                start_time=data["start_time"],
                period=data["period"],
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
    return created, updated


class Command(BaseCommand):
    help = "Sync schedule from hub API or local WEEKLY_SHIFTS → MasseuseShift."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=14,
            help="Days to fetch from hub for pattern extraction (default: 14)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview only — do not write to DB",
        )
        parser.add_argument(
            "--hub-only",
            action="store_true",
            help="Fail if hub API is unavailable (no local fallback)",
        )

    def handle(self, *args, **options):
        days = options["days"]
        dry_run = options["dry_run"]
        hub_only = options["hub_only"]

        masseuse_by_slug = {
            m.slug: m for m in Masseuse.objects.filter(is_active=True)
        }
        default_location = WorkLocation.objects.filter(is_active=True).first()

        source = "hub"
        raw_entries = []
        hub_error = ""

        if not getattr(settings, "HUB_API_KEY", ""):
            hub_error = "HUB_API_KEY is not set on this service"
            source = "local"

        if source == "hub":
            client = HubClient()
            try:
                raw_entries = client.fetch_schedule_json(days=days)
            except HubAPIError as exc:
                hub_error = str(exc)
                if hub_only:
                    self.stderr.write(self.style.ERROR(hub_error))
                    raise SystemExit(1) from exc
                source = "local"
            except HubUnavailableError as exc:
                hub_error = str(exc)
                if hub_only:
                    self.stderr.write(self.style.ERROR(f"Hub unreachable: {exc}"))
                    raise SystemExit(1) from exc
                source = "local"

        if source == "hub":
            patterns = _patterns_from_hub(
                raw_entries, masseuse_by_slug, default_location
            )
        else:
            if hub_error:
                self.stderr.write(
                    self.style.WARNING(
                        f"Hub sync skipped ({hub_error}). "
                        "Using local WEEKLY_SHIFTS. "
                        "To enable hub sync, set HUB_API_KEY on the black-velvet "
                        "web service in Render (SiteConfig.api_key for black-velvet)."
                    )
                )
            patterns = _patterns_from_weekly_shifts(
                masseuse_by_slug, default_location
            )

        if not patterns:
            self.stderr.write(self.style.ERROR("No schedule patterns to sync."))
            raise SystemExit(1)

        if dry_run:
            self.stdout.write(
                f"[dry-run] Would upsert {len(patterns)} MasseuseShift records "
                f"(source: {source})."
            )
            return

        created, updated = _upsert_patterns(patterns)

        if source == "hub":
            self.stdout.write(
                f"Synced {len(raw_entries)} hub entries → "
                f"created {created}, updated {updated} MasseuseShift records."
            )
            self.stdout.write(self.style.SUCCESS("Schedule synced from hub API."))
        else:
            self.stdout.write(
                f"Synced {len(patterns)} local patterns → "
                f"created {created}, updated {updated} MasseuseShift records."
            )
            self.stdout.write(
                self.style.SUCCESS("Schedule synced from local WEEKLY_SHIFTS.")
            )
