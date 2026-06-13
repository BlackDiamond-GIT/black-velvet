import json
from functools import lru_cache
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent / 'seed_data.json'
MEDIA_ROOT = Path(__file__).resolve().parent.parent.parent / 'data' / 'seed_media'

TRANSLATED_FIELDS = {
    'services': (
        'name', 'short_desc', 'description', 'meta_title', 'meta_description',
    ),
    'masseuses': (
        'bio', 'specializations', 'meta_title', 'meta_description',
    ),
    'tags': ('name',),
    'posts': (
        'title', 'excerpt', 'content', 'meta_title', 'meta_description',
    ),
    'faqs': ('question', 'answer'),
    'reviews': ('role', 'text'),
    'price_categories': ('name',),
    'price_items': ('service_name', 'note'),
}


@lru_cache(maxsize=1)
def load_bundle():
    with DATA_PATH.open(encoding='utf-8') as handle:
        return json.load(handle)


def seed_media_path(category, slug):
    path = MEDIA_ROOT / category / f'{slug}.webp'
    if path.is_file():
        return path
    return None


def model_defaults(row, field_names):
    defaults = {}
    for field in field_names:
        if field in row and row[field] is not None:
            defaults[field] = row[field]
        for lang in ('cs', 'en', 'ru'):
            key = f'{field}_{lang}'
            if key in row and row[key] is not None:
                defaults[key] = row[key]
    return defaults


def service_defaults(row):
    fields = (
        'name', 'short_desc', 'description', 'duration_min', 'duration_max',
        'price_czk', 'price_label', 'meta_title', 'meta_description', 'order',
    )
    defaults = model_defaults(row, TRANSLATED_FIELDS['services'])
    for field in fields:
        if field in row:
            defaults[field] = row[field]
    defaults['is_active'] = bool(row.get('is_active', True))
    return defaults


def masseuse_defaults(row):
    defaults = model_defaults(row, TRANSLATED_FIELDS['masseuses'])
    for field in ('years_experience', 'order'):
        if field in row:
            defaults[field] = row[field]
    defaults['is_active'] = bool(row.get('is_active', True))
    return defaults
