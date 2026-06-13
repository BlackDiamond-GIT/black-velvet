"""Booking click aggregates and admin dashboard data."""

from __future__ import annotations

import datetime
from collections import defaultdict
from typing import TYPE_CHECKING, Any, TypedDict
from urllib.parse import urlparse

from django.db.models import Count
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .click_labels import channel_label, placement_label

if TYPE_CHECKING:
    from django.db.models import QuerySet

    from .models import BookingClick

DEFAULT_DAYS = 7
ALLOWED_DAYS = (7, 14, 30)
CHART_HOUR_OF_DAY = "hour_of_day"
CHART_TIMELINE = "timeline"
CHART_DAILY = "daily"
PERIOD_KIND_DAY = "day"
PERIOD_KIND_RANGE = "range"
AUDIENCE_HUMANS = "humans"
AUDIENCE_BOTS = "bots"
AUDIENCE_ALL = "all"
ALLOWED_AUDIENCES = frozenset({AUDIENCE_HUMANS, AUDIENCE_BOTS, AUDIENCE_ALL})


class ChartBar(TypedDict):
    label: str
    count: int
    height_pct: float
    title: str
    is_peak: bool


class TrendPoint(TypedDict):
    x_pct: float
    y_pct: float
    svg_y: float
    label: str
    count: int
    is_peak: bool


class PlacementRow(TypedDict):
    key: str
    label: str
    count: int
    pct: float


class FilterLink(TypedDict):
    label: str
    url: str
    active: bool


class PeriodBounds(TypedDict):
    start: datetime.datetime
    end: datetime.datetime
    period_kind: str
    active_date: datetime.date | None
    period_days: int


class ClickDashboard(TypedDict):
    total: int
    whatsapp_count: int
    reservation_count: int
    human_count: int
    bot_count: int
    peak_label: str
    peak_detail: str
    avg_per_bucket: float
    chart_title: str
    chart_subtitle: str
    chart_mode: str
    bars: list[ChartBar]
    trend_points: list[TrendPoint]
    trend_area_points: str
    trend_line_points: str
    top_placements: list[PlacementRow]
    period_start: datetime.datetime
    period_end: datetime.datetime
    period_days: int
    period_kind: str
    active_date: datetime.date | None
    date_input_value: str
    date_input_max: str
    active_channel: str
    active_placement: str
    period_links: list[FilterLink]
    channel_links: list[FilterLink]
    placement_links: list[FilterLink]
    chart_mode_links: list[FilterLink]
    audience_links: list[FilterLink]
    active_audience: str
    active_summary_parts: list[str]
    today_url: str
    yesterday_url: str
    is_today_active: bool
    is_yesterday_active: bool
    reset_url: str
    humans_filter_url: str
    bots_filter_url: str


def _parse_days(raw: str | None) -> int | None:
    if raw is None or raw == "":
        return None
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return None
    return value if value in ALLOWED_DAYS else None


def _parse_date(raw: str | None) -> datetime.date | None:
    if not raw:
        return None
    try:
        return datetime.date.fromisoformat(raw.strip())
    except ValueError:
        return None


def _local_today() -> datetime.date:
    return timezone.localtime(timezone.now()).date()


def _aware(dt: datetime.datetime) -> datetime.datetime:
    if timezone.is_aware(dt):
        return dt
    return timezone.make_aware(dt, timezone.get_current_timezone())


def _floor_hour(dt: datetime.datetime) -> datetime.datetime:
    return _aware(dt).replace(minute=0, second=0, microsecond=0)


def _calendar_day_bounds(day: datetime.date) -> tuple[datetime.datetime, datetime.datetime]:
    tz = timezone.get_current_timezone()
    start = timezone.make_aware(datetime.datetime.combine(day, datetime.time.min), tz)
    end = start + datetime.timedelta(days=1)
    return start, end


def resolve_period_bounds(get_params: dict[str, str]) -> PeriodBounds:
    parsed_date = _parse_date(get_params.get("date"))
    if parsed_date is not None:
        start, end = _calendar_day_bounds(parsed_date)
        return PeriodBounds(
            start=start,
            end=end,
            period_kind=PERIOD_KIND_DAY,
            active_date=parsed_date,
            period_days=0,
        )

    days = _parse_days(get_params.get("days"))
    if days is not None:
        now = timezone.now()
        end = _floor_hour(now) + datetime.timedelta(hours=1)
        start = end - datetime.timedelta(days=days)
        return PeriodBounds(
            start=start,
            end=end,
            period_kind=PERIOD_KIND_RANGE,
            active_date=None,
            period_days=days,
        )

    today = _local_today()
    start, end = _calendar_day_bounds(today)
    return PeriodBounds(
        start=start,
        end=end,
        period_kind=PERIOD_KIND_DAY,
        active_date=today,
        period_days=0,
    )


def _scale_bars(raw: list[tuple[str, int, str]]) -> list[ChartBar]:
    max_count = max((count for _label, count, _title in raw), default=0)
    bars: list[ChartBar] = []
    for label, count, title in raw:
        height = round(count / max_count * 100, 2) if max_count else 0.0
        bars.append(
            ChartBar(
                label=label,
                count=count,
                height_pct=height,
                title=title,
                is_peak=False,
            )
        )
    return _mark_peak_bars(bars)


def _mark_peak_bars(bars: list[ChartBar]) -> list[ChartBar]:
    if not bars:
        return bars
    peak_count = max(bar["count"] for bar in bars)
    if not peak_count:
        return bars
    marked: list[ChartBar] = []
    for bar in bars:
        marked.append(
            ChartBar(
                label=bar["label"],
                count=bar["count"],
                height_pct=bar["height_pct"],
                title=bar["title"],
                is_peak=bar["count"] == peak_count,
            )
        )
    return marked


def _bars_to_trend(bars: list[ChartBar]) -> list[TrendPoint]:
    if not bars:
        return []
    max_count = max(bar["count"] for bar in bars) or 1
    count = len(bars)
    plot_top = 4.0
    plot_height = 32.0
    points: list[TrendPoint] = []
    for index, bar in enumerate(bars):
        x_pct = round(index / (count - 1) * 100, 2) if count > 1 else 50.0
        y_pct = round(bar["count"] / max_count * 100, 2) if max_count else 0.0
        svg_y = round(plot_top + plot_height - (y_pct / 100.0 * plot_height), 2)
        points.append(
            TrendPoint(
                x_pct=x_pct,
                y_pct=y_pct,
                svg_y=svg_y,
                label=bar["label"],
                count=bar["count"],
                is_peak=False,
            )
        )
    peak_index = max(range(len(points)), key=lambda i: points[i]["count"])
    points[peak_index]["is_peak"] = True
    return points


def _trend_svg_paths(points: list[TrendPoint]) -> tuple[str, str]:
    if not points:
        return "", ""

    svg_height = 40.0
    plot_top = 4.0
    plot_height = 32.0
    baseline = svg_height - 2.0

    coords: list[tuple[float, float]] = []
    for point in points:
        x = point["x_pct"]
        y = plot_top + plot_height - (point["y_pct"] / 100.0 * plot_height)
        coords.append((x, y))

    line_points = " ".join(f"{x},{y}" for x, y in coords)
    if len(coords) == 1:
        x, y = coords[0]
        area_points = f"0,{baseline} {x},{y} 100,{baseline}"
    else:
        first_x = coords[0][0]
        last_x = coords[-1][0]
        middle = " ".join(f"{x},{y}" for x, y in coords)
        area_points = f"{first_x},{baseline} {middle} {last_x},{baseline}"
    return area_points, line_points


def _peak_from_bars(bars: list[ChartBar]) -> str:
    if not bars:
        return "—"
    best = max(bars, key=lambda bar: bar["count"])
    return best["label"] if best["count"] else "—"


def _peak_detail(bars: list[ChartBar]) -> str:
    if not bars:
        return ""
    best = max(bars, key=lambda bar: bar["count"])
    if not best["count"]:
        return ""
    return str(_("%(time)s — %(count)s clicks") % {"time": best["label"], "count": best["count"]})


def _avg_per_bucket(bars: list[ChartBar]) -> float:
    if not bars:
        return 0.0
    total = sum(bar["count"] for bar in bars)
    return round(total / len(bars), 1)


def _filtered_queryset(
    queryset: QuerySet[BookingClick],
    *,
    start: datetime.datetime,
    end: datetime.datetime,
    channel: str = "",
    placement: str = "",
) -> QuerySet[BookingClick]:
    qs = queryset.filter(clicked_at__gte=start, clicked_at__lt=end)
    if channel:
        qs = qs.filter(channel=channel)
    if placement:
        qs = qs.filter(placement=placement)
    return qs


def _timeline_bars(qs: QuerySet[BookingClick], start: datetime.datetime, end: datetime.datetime) -> list[ChartBar]:
    counts: dict[datetime.datetime, int] = defaultdict(int)
    for clicked_at in qs.values_list("clicked_at", flat=True):
        counts[_floor_hour(clicked_at)] += 1

    raw: list[tuple[str, int, str]] = []
    cursor = start
    while cursor < end:
        count = counts.get(cursor, 0)
        local = timezone.localtime(cursor)
        label = local.strftime("%H:00")
        raw.append((label, count, f"{label}: {count}"))
        cursor += datetime.timedelta(hours=1)
    return _scale_bars(raw)


def _hour_of_day_bars(qs: QuerySet[BookingClick]) -> list[ChartBar]:
    buckets = [0] * 24
    for clicked_at in qs.values_list("clicked_at", flat=True):
        buckets[timezone.localtime(clicked_at).hour] += 1
    raw = [
        (f"{hour:02d}:00", buckets[hour], f"{hour:02d}:00–{hour:02d}:59: {buckets[hour]}")
        for hour in range(24)
    ]
    return _scale_bars(raw)


def _daily_bars(qs: QuerySet[BookingClick], start: datetime.datetime, end: datetime.datetime) -> list[ChartBar]:
    counts: dict[datetime.date, int] = defaultdict(int)
    for clicked_at in qs.values_list("clicked_at", flat=True):
        counts[timezone.localtime(clicked_at).date()] += 1

    raw: list[tuple[str, int, str]] = []
    day = timezone.localtime(start).date()
    last = timezone.localtime(end - datetime.timedelta(seconds=1)).date()
    while day <= last:
        count = counts.get(day, 0)
        label = day.strftime("%d.%m")
        raw.append((label, count, f"{day.strftime('%d.%m.%Y')}: {count}"))
        day += datetime.timedelta(days=1)
    return _scale_bars(raw)


def _top_placements(qs: QuerySet[BookingClick], total: int, limit: int = 6) -> list[PlacementRow]:
    rows = (
        qs.values("placement")
        .annotate(count=Count("id"))
        .order_by("-count")[:limit]
    )
    out: list[PlacementRow] = []
    for row in rows:
        count = int(row["count"])
        key = str(row["placement"])
        out.append(
            PlacementRow(
                key=key,
                label=placement_label(key),
                count=count,
                pct=round(count / total * 100, 1) if total else 0.0,
            )
        )
    return out


def parse_audience(raw: str | None) -> str:
    value = (raw or AUDIENCE_HUMANS).strip().lower()
    if value in ALLOWED_AUDIENCES:
        return value
    return AUDIENCE_HUMANS


def filter_queryset_by_audience(
    queryset: QuerySet[BookingClick],
    audience: str,
) -> QuerySet[BookingClick]:
    if audience == AUDIENCE_BOTS:
        return queryset.filter(is_bot=True)
    if audience == AUDIENCE_ALL:
        return queryset
    return queryset.filter(is_bot=False)


def parse_stats_filters(get_params: dict[str, str]) -> dict[str, str | int | None]:
    chart_mode = (get_params.get("chart") or "").strip()
    if chart_mode not in {CHART_HOUR_OF_DAY, CHART_TIMELINE, CHART_DAILY}:
        chart_mode = ""

    bounds = resolve_period_bounds(get_params)
    return {
        "days": bounds["period_days"] if bounds["period_kind"] == PERIOD_KIND_RANGE else None,
        "date": bounds["active_date"].isoformat() if bounds["active_date"] else "",
        "period_kind": bounds["period_kind"],
        "channel": (get_params.get("channel__exact") or get_params.get("click_channel") or "").strip(),
        "placement": (get_params.get("placement__exact") or get_params.get("click_placement") or "").strip(),
        "chart": chart_mode,
        "audience": parse_audience(get_params.get("audience")),
    }


def build_filter_url(path: str, get_params: dict[str, str], **updates: str | None) -> str:
    from urllib.parse import urlencode

    params = dict(get_params)
    for key, value in updates.items():
        if key == "click_channel":
            params.pop("channel__exact", None)
            if value:
                params["channel__exact"] = value
        elif key == "click_placement":
            params.pop("placement__exact", None)
            if value:
                params["placement__exact"] = value
        elif key == "days" and value:
            params.pop("date", None)
            params["days"] = value
        elif key == "date" and value:
            params.pop("days", None)
            params["date"] = value
        elif value is None or value == "":
            params.pop(key, None)
        else:
            params[key] = value
    params.pop("click_channel", None)
    params.pop("click_placement", None)
    params.pop("p", None)
    params.pop("e", None)

    query = urlencode(params, doseq=True)
    return f"{path}?{query}" if query else path


def _build_active_summary(
    *,
    audience: str,
    channel: str,
    placement: str,
    period_kind: str,
    active_date: datetime.date | None,
    period_days: int,
) -> list[str]:
    audience_labels = {
        AUDIENCE_HUMANS: str(_("People")),
        AUDIENCE_BOTS: str(_("Bots")),
        AUDIENCE_ALL: str(_("All traffic")),
    }
    parts = [audience_labels.get(audience, audience)]
    if channel:
        parts.append(channel_label(channel))
    if placement:
        parts.append(placement_label(placement))
    if period_kind == PERIOD_KIND_DAY and active_date:
        parts.append(active_date.strftime("%d.%m.%Y"))
    elif period_days:
        period_labels = {7: str(_("7 days")), 14: str(_("14 days")), 30: str(_("30 days"))}
        parts.append(period_labels.get(period_days, str(_("%(days)s days") % {"days": period_days})))
    return parts


def build_click_dashboard(
    queryset: QuerySet[BookingClick],
    *,
    path: str,
    get_params: dict[str, str],
    source_queryset: QuerySet[BookingClick] | None = None,
) -> ClickDashboard:
    filters = parse_stats_filters(get_params)
    channel = str(filters["channel"])
    placement = str(filters["placement"])
    chart_mode = str(filters["chart"])
    audience = str(filters["audience"])

    bounds = resolve_period_bounds(get_params)
    start = bounds["start"]
    end = bounds["end"]
    period_kind = bounds["period_kind"]
    active_date = bounds["active_date"]
    period_days = bounds["period_days"]

    qs = _filtered_queryset(queryset, start=start, end=end, channel=channel, placement=placement)
    total = qs.count()
    whatsapp_count = qs.filter(channel="whatsapp").count()
    reservation_count = qs.filter(channel="reservation").count()

    period_base = _filtered_queryset(
        source_queryset if source_queryset is not None else queryset,
        start=start,
        end=end,
        channel=channel,
        placement=placement,
    )
    human_count = period_base.filter(is_bot=False).count()
    bot_count = period_base.filter(is_bot=True).count()

    bucket_label = str(_("hour"))
    if period_kind == PERIOD_KIND_DAY:
        chart_mode = CHART_TIMELINE
        bars = _timeline_bars(qs, start, end)
        date_label = active_date.strftime("%d.%m.%Y") if active_date else ""
        chart_title = str(_("Clicks on %(date)s (by hour)") % {"date": date_label})
        chart_subtitle = str(_("Each bar = one hour, Prague time"))
    elif chart_mode == CHART_DAILY:
        bars = _daily_bars(qs, start, end)
        chart_title = str(_("Clicks by day"))
        chart_subtitle = str(_("Each bar = one calendar day"))
        bucket_label = str(_("day"))
    else:
        chart_mode = CHART_HOUR_OF_DAY
        bars = _hour_of_day_bars(qs)
        chart_title = str(_("Peak hours (0–23)"))
        chart_subtitle = str(_("Summed over the selected period · Prague time"))

    trend_points = _bars_to_trend(bars)
    trend_area_points, trend_line_points = _trend_svg_paths(trend_points)
    avg_per_bucket = _avg_per_bucket(bars)
    peak_detail = _peak_detail(bars)

    if peak_detail and avg_per_bucket:
        chart_subtitle = f"{chart_subtitle} · {peak_detail} · {_('Avg per %(unit)s: %(avg)s') % {'unit': bucket_label, 'avg': avg_per_bucket}}"

    if audience == AUDIENCE_HUMANS and bot_count:
        chart_subtitle = (
            f"{chart_subtitle} · {_('%(count)s bot clicks excluded') % {'count': bot_count}}"
        )

    today = _local_today()
    yesterday = today - datetime.timedelta(days=1)

    period_labels = {7: str(_("7 days")), 14: str(_("14 days")), 30: str(_("30 days"))}
    period_links: list[FilterLink] = []
    for option in ALLOWED_DAYS:
        period_links.append(
            FilterLink(
                label=period_labels[option],
                url=build_filter_url(path, get_params, days=str(option)),
                active=period_kind == PERIOD_KIND_RANGE and period_days == option,
            )
        )

    today_url = build_filter_url(path, get_params, date=today.isoformat(), days=None)
    yesterday_url = build_filter_url(path, get_params, date=yesterday.isoformat(), days=None)

    channel_options = [
        ("", str(_("All channels"))),
        ("whatsapp", channel_label("whatsapp")),
        ("reservation", channel_label("reservation")),
    ]
    channel_links = [
        FilterLink(
            label=label,
            url=build_filter_url(path, get_params, click_channel=key or None),
            active=key == channel,
        )
        for key, label in channel_options
    ]

    placement_rows = (
        _filtered_queryset(queryset, start=start, end=end, channel=channel, placement="")
        .values("placement")
        .annotate(count=Count("id"))
        .order_by("-count")[:8]
    )
    placement_links: list[FilterLink] = [
        FilterLink(
            label=str(_("All buttons")),
            url=build_filter_url(path, get_params, click_placement=None),
            active=not placement,
        )
    ]
    for row in placement_rows:
        key = str(row["placement"])
        placement_links.append(
            FilterLink(
                label=f"{placement_label(key)} ({row['count']})",
                url=build_filter_url(path, get_params, click_placement=key),
                active=key == placement,
            )
        )

    chart_mode_links: list[FilterLink] = []
    if period_kind == PERIOD_KIND_RANGE:
        chart_mode_links = [
            FilterLink(
                label=str(_("Peak hours")),
                url=build_filter_url(path, get_params, chart=CHART_HOUR_OF_DAY),
                active=chart_mode == CHART_HOUR_OF_DAY,
            ),
            FilterLink(
                label=str(_("By day")),
                url=build_filter_url(path, get_params, chart=CHART_DAILY),
                active=chart_mode == CHART_DAILY,
            ),
        ]

    audience_options = [
        (AUDIENCE_HUMANS, str(_("People"))),
        (AUDIENCE_BOTS, str(_("Bots"))),
        (AUDIENCE_ALL, str(_("All traffic"))),
    ]
    audience_links = [
        FilterLink(
            label=label,
            url=build_filter_url(path, get_params, audience=key),
            active=key == audience,
        )
        for key, label in audience_options
    ]

    reset_url = build_filter_url(
        path,
        get_params,
        days=None,
        date=None,
        chart=None,
        audience=None,
        click_channel=None,
        click_placement=None,
    )

    date_input_value = active_date.isoformat() if active_date else today.isoformat()

    return ClickDashboard(
        total=total,
        whatsapp_count=whatsapp_count,
        reservation_count=reservation_count,
        human_count=human_count,
        bot_count=bot_count,
        peak_label=_peak_from_bars(bars),
        peak_detail=peak_detail,
        avg_per_bucket=avg_per_bucket,
        chart_title=chart_title,
        chart_subtitle=chart_subtitle,
        chart_mode=chart_mode,
        bars=bars,
        trend_points=trend_points,
        trend_area_points=trend_area_points,
        trend_line_points=trend_line_points,
        top_placements=_top_placements(qs, total),
        period_start=start,
        period_end=end,
        period_days=period_days,
        period_kind=period_kind,
        active_date=active_date,
        date_input_value=date_input_value,
        date_input_max=today.isoformat(),
        active_channel=channel,
        active_placement=placement,
        period_links=period_links,
        channel_links=channel_links,
        placement_links=placement_links,
        chart_mode_links=chart_mode_links,
        audience_links=audience_links,
        active_audience=audience,
        active_summary_parts=_build_active_summary(
            audience=audience,
            channel=channel,
            placement=placement,
            period_kind=period_kind,
            active_date=active_date,
            period_days=period_days,
        ),
        today_url=today_url,
        yesterday_url=yesterday_url,
        is_today_active=period_kind == PERIOD_KIND_DAY and active_date == today,
        is_yesterday_active=period_kind == PERIOD_KIND_DAY and active_date == yesterday,
        reset_url=reset_url,
        humans_filter_url=build_filter_url(path, get_params, audience=AUDIENCE_HUMANS),
        bots_filter_url=build_filter_url(path, get_params, audience=AUDIENCE_BOTS),
    )


def format_page_path(raw: str) -> str:
    """Short display path for admin list."""
    value = (raw or "").strip()
    if not value:
        return "—"
    if value.startswith("http"):
        parsed = urlparse(value)
        return parsed.path or value
    return value


# Backwards compatibility for tests
def hourly_click_bars(
    queryset: QuerySet[BookingClick],
    *,
    days: int = DEFAULT_DAYS,
    channel: str = "",
    placement: str = "",
    date: str | None = None,
) -> tuple[list[dict[str, Any]], datetime.datetime, datetime.datetime, int]:
    params: dict[str, str] = {"channel__exact": channel, "placement__exact": placement}
    if date:
        params["date"] = date
    elif days in ALLOWED_DAYS:
        params["days"] = str(days)
    else:
        params["date"] = _local_today().isoformat()

    dash = build_click_dashboard(queryset, path="/", get_params=params)
    legacy_bars = [
        {
            "label": bar["label"],
            "count": bar["count"],
            "height_pct": bar["height_pct"],
            "bucket": None,
        }
        for bar in dash["bars"]
    ]
    return legacy_bars, dash["period_start"], dash["period_end"], dash["total"]
