import math
from datetime import datetime

from apps.team.models import Masseuse

# Black Velvet: apps/schedule/schedule_data.py
TIMES = ['09:00', '11:00', '18:30', '20:30', '02:00', '04:00', '06:00']

DAYS_SHORT = {
    'cs': ['Po', 'Út', 'St', 'Čt', 'Pá', 'So', 'Ne'],
    'en': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'ru': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
}


def today_weekday_index():
    return datetime.now().weekday()


def _srand(seed):
    x = math.sin(seed + 1) * 10000
    return x - math.floor(x)


def _slot_dict(slot_id, masseuse, service, is_booked):
    return {
        'id': slot_id,
        'masseuse_id': masseuse.id,
        'masseuse_name': masseuse.name,
        'service_name': service.name,
        'is_booked': is_booked,
    }


def build_demo_grid(masseuses):
    grid = {day: {time: [] for time in TIMES} for day in range(7)}
    seed = 77
    slot_id = 1

    for masseuse in masseuses:
        services = list(masseuse.services.filter(is_active=True))
        if not services:
            continue

        for day in range(7):
            for time in TIMES:
                seed += 1
                if _srand(seed) <= 0.42:
                    continue

                seed += 1
                service = services[int(_srand(seed + 500) * len(services)) % len(services)]
                seed += 1
                is_booked = _srand(seed + 1000) > 0.52

                grid[day][time].append(
                    _slot_dict(slot_id, masseuse, service, is_booked)
                )
                slot_id += 1

    return grid


def build_schedule_rows(grid, today_idx):
    rows = []
    for time in TIMES:
        cells = []
        for day in range(7):
            cells.append({
                'day': day,
                'is_today': day == today_idx,
                'slots': grid[day][time],
            })
        rows.append({'time': time, 'cells': cells})
    return rows


def build_masseuse_schedules(grid, masseuses, days_short, today_idx):
    schedules = []

    for masseuse in masseuses:
        days = []
        for day_idx in range(7):
            slots = []
            for time in TIMES:
                for slot in grid[day_idx][time]:
                    if slot['masseuse_id'] != masseuse.id:
                        continue
                    slots.append({
                        'time': time,
                        'service_name': slot['service_name'],
                        'is_booked': slot['is_booked'],
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
    masseuses = Masseuse.objects.filter(is_active=True).prefetch_related('services')
    today_idx = today_weekday_index()
    grid = build_demo_grid(masseuses)
    days_short = DAYS_SHORT.get(lang, DAYS_SHORT['cs'])

    return {
        'masseuses': masseuses,
        'masseuse_schedules': build_masseuse_schedules(grid, masseuses, days_short, today_idx),
        'today_idx': today_idx,
    }
