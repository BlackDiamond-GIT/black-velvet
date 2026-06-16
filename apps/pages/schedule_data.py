# Black Velvet weekly shifts — source: https://tantra-prague.com/cs/rozvrh/
# Only Black Velvet 🖤 entries; weekday 0 = Monday … 6 = Sunday.
# Address: Lužická 1416/29 (see SITE_ADDRESS in settings).

TANTRA_SLUG_MAP = {
    'julia': 'julia',
    'diana': 'diana',
    'laura': 'laura',
    'vanessa': 'vanessa',
    'ella': 'ella',
    'anna': 'mira',
}

PERIOD_LABELS = {
    'day': {'cs': 'Den', 'en': 'Day', 'ru': 'День'},
    'night': {'cs': 'Noc', 'en': 'Night', 'ru': 'Ночь'},
}

# Recurring weekly pattern (Út 16 – Ne 21 červen 2026 on tantra-prague.com).
WEEKLY_SHIFTS = {
    'julia': {
        1: [{'start': '09:00', 'end': '20:30', 'period': 'day'}],
        2: [{'start': '09:00', 'end': '20:30', 'period': 'day'}],
    },
    'diana': {
        1: [{'start': '09:00', 'end': '20:30', 'period': 'day'}],
        2: [{'start': '09:00', 'end': '20:30', 'period': 'day'}],
        5: [{'start': '09:00', 'end': '20:30', 'period': 'day'}],
    },
    'laura': {
        3: [{'start': '18:30', 'end': '04:00', 'period': 'night'}],
    },
    'mira': {
        5: [{'start': '09:00', 'end': '20:30', 'period': 'day'}],
    },
}
