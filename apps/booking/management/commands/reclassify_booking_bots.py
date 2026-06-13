"""Retroactively mark suspicious booking clicks as bot traffic."""

from __future__ import annotations

import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.booking.bot_reclassify import apply_reclassification, day_queryset, top_noisy_fingerprints
from apps.booking.models import BookingClick


class Command(BaseCommand):
    help = "Reclassify high-volume booking clicks as bot traffic (rate heuristics)."

    def add_arguments(self, parser: object) -> None:
        parser.add_argument(
            "--date",
            type=str,
            default="",
            help="Prague calendar day to scan (YYYY-MM-DD). Default: all records.",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="Write is_bot=True to DB (default: dry-run only).",
        )

    def handle(self, *args: object, **options: object) -> None:
        dry_run = not bool(options["apply"])
        date_raw = str(options["date"] or "").strip()

        qs = BookingClick.objects.all()
        if date_raw:
            try:
                day = datetime.date.fromisoformat(date_raw)
            except ValueError:
                self.stderr.write(self.style.ERROR(f"Invalid --date: {date_raw}"))
                return
            qs = day_queryset(qs, day)
            scope_label = day.isoformat()
        else:
            scope_label = "all time"

        humans_before = qs.filter(is_bot=False).count()
        bots_before = qs.filter(is_bot=True).count()

        result = apply_reclassification(qs, dry_run=dry_run)

        mode = "DRY-RUN" if dry_run else "APPLIED"
        self.stdout.write(f"\n[{mode}] Reclassify booking bots — scope: {scope_label}\n")
        self.stdout.write(f"  Records in scope:     {qs.count()}")
        self.stdout.write(f"  Humans before:        {humans_before}")
        self.stdout.write(f"  Bots before:          {bots_before}")
        self.stdout.write(f"  To mark as bot:       {result.total_marked}")
        self.stdout.write(f"    hourly (ip_hash):   {len(result.hourly_ip_hash_ids)}")
        self.stdout.write(f"    daily (ip_hash):    {len(result.daily_ip_hash_ids)}")
        self.stdout.write(f"    hourly (ip_only):   {len(result.hourly_ip_only_ids)}")
        self.stdout.write(f"    daily (ip_only):    {len(result.daily_ip_only_ids)}")

        if not dry_run:
            humans_after = qs.filter(is_bot=False).count()
            bots_after = qs.filter(is_bot=True).count()
            self.stdout.write(f"  Humans after:         {humans_after}")
            self.stdout.write(f"  Bots after:           {bots_after}")
        else:
            self.stdout.write("\n  Run with --apply to persist changes.")

        noisy = top_noisy_fingerprints(qs, limit=5)
        if noisy:
            self.stdout.write("\n  Top noisy fingerprints (ip_hash prefix):")
            for prefix, count in noisy:
                self.stdout.write(f"    {prefix}  {count}")

        if date_raw and not dry_run:
            today = timezone.localtime(timezone.now()).date()
            self.stdout.write(f"\n  Done for {scope_label} (today Prague: {today}).")
