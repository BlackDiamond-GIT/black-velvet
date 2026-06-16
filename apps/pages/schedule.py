from datetime import datetime, time
from zoneinfo import ZoneInfo

from apps.team.models import Masseuse

from .models import MasseuseShift
from .schedule_data import PERIOD_LABELS, WEEKLY_SHIFTS

PRAGUE_TZ = ZoneInfo('Europe/Prague')

DAYS_SHORT = {
    'cs': ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'],
    'en': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'ru': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
}


def prague_now():
    return datetime.now(PRAGUE_TZ)


def today_weekday_index(now=None):
    return (now or prague_now()).weekday()


def _period_label(period, lang):
    labels = PERIOD_LABELS.get(period, {})
    return labels.get(lang) or labels.get('cs', period)


def _time_to_minutes(value):
    if isinstance(value, time):
        return value.hour * 60 + value.minute
    hour, minute = map(int, str(value).split(':'))
    return hour * 60 + minute


def _shift_time_display(start, end):
    if isinstance(start, time):
        start = start.strftime('%H:%M')
    if isinstance(end, time):
        end = end.strftime('%H:%M')
    return f'{start}–{end}'


def _is_overnight(start, end):
    return _time_to_minutes(end) <= _time_to_minutes(start)


def _shift_record(shift, day_idx, lang, *, is_overnight_tail=False):
    start = shift['start']
    end = shift['end']
    if is_overnight_tail:
        time_display = _shift_time_display('00:00', end)
    else:
        time_display = _shift_time_display(start, end)

    return {
        'time': time_display,
        'period': shift['period'],
        'period_label': _period_label(shift['period'], lang),
        'is_overnight_tail': is_overnight_tail,
        'is_booked': False,
        'day_idx': day_idx,
    }


def _shifts_from_db():
    records = (
        MasseuseShift.objects.filter(is_active=True)
        .select_related('masseuse')
        .order_by('weekday', 'order', 'start_time')
    )
    grouped = {}
    for row in records:
        if not row.masseuse.is_active:
            continue
        grouped.setdefault(row.masseuse.slug, {}).setdefault(row.weekday, []).append({
            'start': row.start_time.strftime('%H:%M'),
            'end': row.end_time.strftime('%H:%M'),
            'period': row.period,
        })
    return grouped


def _shifts_source():
    db_shifts = _shifts_from_db()
    if db_shifts:
        return db_shifts
    return WEEKLY_SHIFTS


def _shift_is_active_now(shift, weekday, now_mins, today_idx, yesterday_idx):
    start_mins = _time_to_minutes(shift['start'])
    end_mins = _time_to_minutes(shift['end'])
    overnight = _is_overnight(shift['start'], shift['end'])

    if weekday == today_idx:
        if overnight:
            return now_mins >= start_mins
        return start_mins <= now_mins < end_mins

    if overnight and weekday == yesterday_idx:
        return now_mins < end_mins

    return False


def get_active_shifts(lang='cs'):
    now = prague_now()
    today_idx = now.weekday()
    yesterday_idx = (today_idx - 1) % 7
    now_mins = now.hour * 60 + now.minute
    shifts_by_slug = _shifts_source()
    slug_map = {
        m.slug: m
        for m in Masseuse.objects.filter(is_active=True, slug__in=shifts_by_slug.keys())
    }

    active = []
    for slug, day_shifts in shifts_by_slug.items():
        masseuse = slug_map.get(slug)
        if not masseuse:
            continue

        for weekday, shifts in day_shifts.items():
            for shift in shifts:
                if not _shift_is_active_now(
                    shift, weekday, now_mins, today_idx, yesterday_idx
                ):
                    continue

                active.append({
                    'masseuse': masseuse,
                    'time': _shift_time_display(shift['start'], shift['end']),
                    'period': shift['period'],
                    'period_label': _period_label(shift['period'], lang),
                })

    return active


def build_schedule_grid(masseuses, lang='cs'):
    slug_map = {m.slug: m for m in masseuses}
    grid = {day: [] for day in range(7)}
    slot_id = 1

    for slug, days in _shifts_source().items():
        masseuse = slug_map.get(slug)
        if not masseuse:
            continue

        for day_idx in range(7):
            day_shifts = days.get(day_idx, [])
            slots = []
            for shift in day_shifts:
                slots.append(_shift_record(shift, day_idx, lang))

            prev_day = (day_idx - 1) % 7
            for shift in days.get(prev_day, []):
                if _is_overnight(shift['start'], shift['end']):
                    slots.append(
                        _shift_record(shift, day_idx, lang, is_overnight_tail=True)
                    )

            for slot in sorted(slots, key=lambda item: item['time']):
                grid[day_idx].append({
                    'id': slot_id,
                    'masseuse_id': masseuse.id,
                    'masseuse_name': masseuse.name,
                    'time': slot['time'],
                    'period': slot['period'],
                    'period_label': slot['period_label'],
                    'is_overnight_tail': slot['is_overnight_tail'],
                    'is_booked': False,
                })
                slot_id += 1

    return grid


def build_masseuse_schedules(masseuses, lang, days_short, today_idx):
    schedules = []
    shifts_by_slug = _shifts_source()
    scheduled_slugs = set(shifts_by_slug.keys())

    for masseuse in masseuses:
        if masseuse.slug not in scheduled_slugs:
            continue

        day_shifts = shifts_by_slug.get(masseuse.slug, {})
        days = []

        for day_idx in range(7):
            slots = []
            for shift in day_shifts.get(day_idx, []):
                slots.append(_shift_record(shift, day_idx, lang))

            for prev_day, prev_shifts in day_shifts.items():
                if prev_day != (day_idx - 1) % 7:
                    continue
                for shift in prev_shifts:
                    if _is_overnight(shift['start'], shift['end']):
                        slots.append(
                            _shift_record(shift, day_idx, lang, is_overnight_tail=True)
                        )

            slots.sort(key=lambda item: item['time'])

            days.append({
                'index': day_idx,
                'label': days_short[day_idx],
                'is_today': day_idx == today_idx,
                'slots': slots,
            })

        schedules.append({
            'masseuse': masseuse,
            'days': days,
        })

    return schedules


def get_schedule_context(lang='cs'):
    shifts_by_slug = _shifts_source()
    scheduled_slugs = list(shifts_by_slug.keys())
    masseuses = (
        Masseuse.objects.filter(is_active=True, slug__in=scheduled_slugs)
        .prefetch_related('services')
    )
    now = prague_now()
    today_idx = now.weekday()
    days_short = DAYS_SHORT.get(lang, DAYS_SHORT['cs'])

    return {
        'masseuses': masseuses,
        'masseuse_schedules': build_masseuse_schedules(
            masseuses, lang, days_short, today_idx
        ),
        'active_shifts': get_active_shifts(lang),
        'today_idx': today_idx,
        'current_time': now.strftime('%H:%M'),
    }
