import ast
import importlib.util
import json
from pathlib import Path

VELVET_ROOT = Path('/Users/olegbonislavskyi/Sites/black-velvet/black-velvet')

SERVICE_SLUG_MAP = {
    'aromaterapie': 'aromaterapeuticka-masaz',
    'klasicka-masaz': 'klasicka-masaz',
    'sportovni-masaz': 'sportovni-masaz',
    'thajska-masaz': 'relaxacni-masaz',
    'lymfaticka-masaz': 'lymfaticka-masaz',
    'cbd-relaxacni-masaz': 'relax-masaz',
}

MASSEUSE_SLUG_MAP = {
    'elena': 'elena',
    'lucie': 'lucie',
    'natalia': 'natalie',
    'klara': 'klara',
    'veronika': 'sofia',
    'marketa': 'anna',
}

OLD_BLOG_SLUGS = (
    'lymfaticka-masaz',
    'prvni-masaz-spa',
    'sportovni-vs-relaxacni',
)


def rebrand(text):
    return text


def markdown_to_html(text):
    if not text:
        return ''
    blocks = text.split('\n\n')
    html_parts = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block.startswith('## '):
            html_parts.append(f'<h2>{block[3:]}</h2>')
        else:
            html_parts.append(f'<p>{block}</p>')
    return '\n'.join(html_parts)


def short_desc_from_description(description, max_len=300):
    if not description:
        return ''
    desc = description.strip()
    if len(desc) <= max_len:
        return desc
    cut = desc[:max_len].rsplit(' ', 1)[0]
    return f'{cut}…'


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _extract_posts_data(path):
    source = path.read_text(encoding='utf-8')
    marker = 'posts_data = ['
    start = source.index(marker) + len('posts_data = ')
    depth = 0
    end = start
    for i, char in enumerate(source[start:], start=start):
        if char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    return ast.literal_eval(source[start:end])


def ensure_velvet_root():
    img_root = VELVET_ROOT / 'static' / 'img'
    if not img_root.is_dir():
        raise FileNotFoundError(
            f'Velvet static images not found at {img_root}. '
            f'Check VELVET_ROOT in apps/core/velvet_loader.py.'
        )
    return VELVET_ROOT


def load_services():
    path = VELVET_ROOT / 'apps/services/fixtures/services.json'
    with path.open(encoding='utf-8') as handle:
        fixtures = json.load(handle)
    services = []
    for item in fixtures:
        fields = item['fields']
        velvet_slug = fields['slug']
        slug = SERVICE_SLUG_MAP.get(velvet_slug)
        if not slug:
            continue
        services.append({
            'velvet_slug': velvet_slug,
            'slug': slug,
            'name_cs': rebrand(fields['name_cs']),
            'name_en': rebrand(fields['name_en']),
            'name_ru': rebrand(fields['name_ru']),
            'description_cs': rebrand(fields['description_cs']),
            'description_en': rebrand(fields['description_en']),
            'description_ru': rebrand(fields['description_ru']),
            'short_desc_cs': short_desc_from_description(fields['description_cs']),
            'short_desc_en': short_desc_from_description(fields['description_en']),
            'short_desc_ru': short_desc_from_description(fields['description_ru']),
            'duration': fields['duration_minutes'],
            'price_czk': fields['base_price'],
            'meta_title_cs': rebrand(fields['meta_title']),
            'meta_title_en': rebrand(fields.get('meta_title', fields['meta_title'])),
            'meta_title_ru': rebrand(fields.get('meta_title', fields['meta_title'])),
            'meta_description_cs': rebrand(fields['meta_description']),
            'meta_description_en': rebrand(fields['meta_description']),
            'meta_description_ru': rebrand(fields['meta_description']),
            'order': fields['order'],
        })
    return services


def load_masseuses():
    catalog_path = VELVET_ROOT / 'apps/masseurs/seed_catalog.py'
    content_path = VELVET_ROOT / 'apps/masseurs/seed_content.py'
    catalog_mod = _load_module(catalog_path, 'velvet_masseuse_catalog')
    content_mod = _load_module(content_path, 'velvet_masseuse_content')

    masseuses = []
    for item in catalog_mod.MASSEUSE_CATALOG:
        velvet_slug = item['slug']
        slug = MASSEUSE_SLUG_MAP.get(velvet_slug)
        if not slug:
            continue
        generated = content_mod.generate_masseuse_content(item)
        masseuses.append({
            'velvet_slug': velvet_slug,
            'slug': slug,
            'name': item['name'],
            'bio_cs': rebrand(generated['bio_cs']),
            'bio_en': rebrand(generated['bio_en']),
            'bio_ru': rebrand(generated['bio_ru']),
            'specializations_cs': item['spec_cs'],
            'specializations_en': item['spec_en'],
            'specializations_ru': item['spec_ru'],
            'years_experience': item['exp_years'],
            'meta_title_cs': rebrand(generated['meta_title']),
            'meta_title_en': rebrand(generated['meta_title']),
            'meta_title_ru': rebrand(generated['meta_title']),
            'meta_description_cs': rebrand(generated['meta_description']),
            'meta_description_en': rebrand(generated['meta_description']),
            'meta_description_ru': rebrand(generated['meta_description']),
            'service_slugs': [
                SERVICE_SLUG_MAP[slug]
                for slug in item['service_slugs']
                if slug in SERVICE_SLUG_MAP
            ],
            'order': item['order'] - 1,
        })
    return masseuses


def load_blog_posts():
    path = VELVET_ROOT / 'apps/blog/management/commands/create_initial_posts.py'
    raw_posts = _extract_posts_data(path)
    posts = []
    for item in raw_posts:
        posts.append({
            'slug': item['slug'],
            'title_cs': rebrand(item['title_cs']),
            'title_en': rebrand(item['title_en']),
            'title_ru': rebrand(item['title_ru']),
            'excerpt_cs': rebrand(item['excerpt_cs']),
            'excerpt_en': rebrand(item['excerpt_en']),
            'excerpt_ru': rebrand(item['excerpt_ru']),
            'content_cs': markdown_to_html(rebrand(item['content_cs'])),
            'content_en': markdown_to_html(rebrand(item['content_en'])),
            'content_ru': markdown_to_html(rebrand(item['content_ru'])),
        })
    return posts


def velvet_image_path(category, slug):
    return VELVET_ROOT / 'static' / 'img' / category / f'{slug}.webp'
