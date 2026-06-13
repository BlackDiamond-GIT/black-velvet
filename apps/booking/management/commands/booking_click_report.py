"""Report booking click counts by placement."""

from __future__ import annotations

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone

from apps.booking.models import BookingClick


class Command(BaseCommand):
    help = "Print booking click totals grouped by placement for the last N days."

    def add_arguments(self, parser: object) -> None:
        parser.add_argument(
            "--days",
            type=int,
            default=7,
            help="Look back window in days (default: 7)",
        )
        parser.add_argument(
            "--humans-only",
            action="store_true",
            help="Exclude bot traffic (is_bot=True), matching admin default.",
        )

    def handle(self, *args: object, **options: object) -> None:
        days = int(options["days"])
        humans_only = bool(options["humans_only"])
        since = timezone.now() - timedelta(days=days)
        base = BookingClick.objects.filter(clicked_at__gte=since)
        if humans_only:
            base = base.filter(is_bot=False)
        qs = (
            base.values("placement", "channel")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
        rows = list(qs)
        grand = sum(row["total"] for row in rows)

        audience = "people only" if humans_only else "all traffic"
        self.stdout.write(
            f"Booking clicks since {since:%Y-%m-%d} ({days} days, {audience}): {grand}\n"
        )
        if not rows:
            self.stdout.write("No clicks recorded.")
            return

        self.stdout.write(f"{'TOTAL':>6}  {'CHANNEL':<12}  PLACEMENT")
        self.stdout.write("-" * 48)
        for row in rows:
            pct = (row["total"] / grand * 100) if grand else 0
            self.stdout.write(
                f"{row['total']:>6}  {row['channel']:<12}  {row['placement']}  ({pct:.1f}%)"
            )
