import re

DURATION_TABS = (30, 60, 90)


def _duration_minutes(duration):
    numbers = [int(value) for value in re.findall(r'\d+', duration or '')]
    return numbers[0] if numbers else None


def _tab_for_duration(duration):
    minutes = _duration_minutes(duration)
    if minutes is None:
        return None
    if minutes <= 30:
        return 30
    if minutes <= 60:
        return 60
    return 90


def build_duration_panels(categories):
    grouped = {minutes: [] for minutes in DURATION_TABS}

    for category in categories:
        for item in category.items.all():
            tab = _tab_for_duration(item.duration)
            if tab is None:
                continue
            grouped[tab].append({
                'item': item,
                'category': category.name,
            })

    panels = []
    for minutes in DURATION_TABS:
        entries = grouped[minutes]
        if not entries:
            continue
        panels.append({
            'minutes': minutes,
            'entries': entries,
        })

    return panels
