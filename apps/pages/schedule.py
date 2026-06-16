from datetime import datetime

from apps.team.models import Masseuse

from .schedule_data import PERIOD_LABELS, WEEKLY_SHIFTS

DAYS_SHORT = {
    'cs': ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'],
    'en': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'ru': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
}


def today_weekday_index():
    return datetime.now().weekday()


def _period_label(period, lang):
    labels = PERIOD_LABELS.get(period, {})
    return labels.get(lang) or labels.get('cs', period)


def _shift_time_display(shift):
    return f"{shift['start']}–{shift['end']}"


def build_schedule_grid(masseuses, lang='cs'):
    slug_map = {m.slug: m for m in masseuses}
    grid = {day: [] for day in range(7)}
    slot_id = 1

    for slug, days in WEEKLY_SHIFTS.items():
        masseuse = slug_map.get(slug)
        if not masseuse:
            continue

        for day_idx, shifts in days.items():
            for shift in shifts:
                grid[day_idx].append({
                    'id': slot_id,
                    'masseuse_id': masseuse.id,
                    'masseuse_name': masseuse.name,
                    'time': _shift_time_display(shift),
                    'period': shift['period'],
                    'period_label': _period_label(shift['period'], lang),
                    'is_booked': False,
                })
                slot_id += 1

    return grid


def build_masseuse_schedules(masseuses, lang, days_short, today_idx):
    schedules = []
    scheduled_slugs = set(WEEKLY_SHIFTS.keys())

    for masseuse in masseuses:
        if masseuse.slug not in scheduled_slugs:
            continue

        day_shifts = WEEKLY_SHIFTS.get(masseuse.slug, {})
        days = []

        for day_idx in range(7):
            slots = []
            for shift in day_shifts.get(day_idx, []):
                slots.append({
                    'time': _shift_time_display(shift),
                    'period': shift['period'],
                    'period_label': _period_label(shift['period'], lang),
                    'is_booked': False,
                })

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
    scheduled_slugs = list(WEEKLY_SHIFTS.keys())
    masseuses = (
        Masseuse.objects.filter(is_active=True, slug__in=scheduled_slugs)
        .prefetch_related('services')
    )
    today_idx = today_weekday_index()
    days_short = DAYS_SHORT.get(lang, DAYS_SHORT['cs'])

    return {
        'masseuses': masseuses,
        'masseuse_schedules': build_masseuse_schedules(
            masseuses, lang, days_short, today_idx
        ),
        'today_idx': today_idx,
    }
