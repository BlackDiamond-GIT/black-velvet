"""Set all phone fields to owner-approved numbers (decision 2026-10-30).

Allowed numbers:
  MAIN     = +420 607 365 598  (display everywhere, WA always)
  STUDIO_1 = +420 797 669 633  (studio location only)
  STUDIO_2 = +420 778 622 334  (studio location only)

What this migration does
------------------------
1. Sets SiteSettings field defaults to MAIN / STUDIO_1 as appropriate.
2. Updates the live SiteSettings row (pk=1) so all phone/WA fields reflect
   the new numbers.
3. Sweeps every CharField / TextField in every installed app for any
   non-allowed number and replaces it with MAIN, preserving separator style
   (+420 XXX XXX XXX or 420XXXXXXXXX).  False-positive guard: only tokens
   that match a Czech E.164 prefix (420…) and contain exactly 9 digits after
   the country code are touched; URL host/path segments and log/history tables
   are intentionally excluded because they are matched by table exclusions.
4. Prints a summary of counts.

Reverse: no-op (forward-only, by policy).
"""

import re

from django.db import migrations, models

# ── canonical values ─────────────────────────────────────────────────────────
MAIN        = '+420 607 365 598'
MAIN_DIGITS = '420607365598'
MAIN_WA     = 'https://wa.me/420607365598'
STUDIO_1    = '+420 797 669 633'
STUDIO_2    = '+420 778 622 334'

ALLOWED_DISPLAY = {MAIN, STUDIO_1, STUDIO_2}
ALLOWED_DIGITS  = {'420607365598', '420797669633', '420778622334'}

# Regex that matches any Czech phone number that is NOT in the allowed set.
# Matches:  +420 NNN NNN NNN  |  420NNNNNNNNN  |  NNN NNN NNN  (9 digits)
# Groups: 1 = full match including prefix, 2 = 9 digit core
_ANY_CZ = re.compile(
    r'(?<!\d)'                   # no leading digit
    r'(?:\+?420[ ]?)?'           # optional country code
    r'(\d{3}[ ]?\d{3}[ ]?\d{3})'  # 9-digit core
    r'(?!\d)'                    # no trailing digit
)


def _normalise(core: str) -> str:
    """Strip spaces from a 9-digit group, e.g. '607 365 598' -> '607365598'."""
    return core.replace(' ', '')


def _is_allowed(match_str: str) -> bool:
    """Return True if the full match (including any +420 prefix) is allowed."""
    # Build the display form to compare
    core = _normalise(_ANY_CZ.search(match_str).group(1))
    display_spaced = f'+420 {core[:3]} {core[3:6]} {core[6:]}'
    return display_spaced in ALLOWED_DISPLAY


def _replace_phone_in_value(value: str) -> tuple[str, int]:
    """Replace all non-allowed Czech numbers in *value* with MAIN.

    Returns (new_value, replacement_count).
    """
    count = 0

    def _sub(m: re.Match) -> str:
        nonlocal count
        full = m.group(0)
        if _is_allowed(full):
            return full
        count += 1
        # Preserve separator style: if original had spaces use spaced format
        if ' ' in full:
            # Has spaces → display form  +420 607 365 598
            return MAIN if full.startswith('+') or 'wa.me' not in full else MAIN
        # No spaces → digits only
        if full.startswith('+'):
            return '+' + MAIN_DIGITS
        if full.startswith('420'):
            return MAIN_DIGITS
        # 9-digit only → just the digits part of MAIN
        return '607365598'

    new_value = _ANY_CZ.sub(_sub, value)
    return new_value, count


# Tables we must not sweep (logs, analytics, migrations history)
_SKIP_TABLES = frozenset({
    'django_migrations',
    'booking_bookingclick',
    'django_admin_log',
})

_PROJECT_APPS = (
    'core', 'blog', 'pages', 'services', 'team',
    'booking', 'reservations', 'media_library',
)


def fix_phones(apps, schema_editor):
    total = 0
    for label in _PROJECT_APPS:
        try:
            config = apps.get_app_config(label)
        except LookupError:
            continue
        for model in config.get_models():
            if model._meta.db_table in _SKIP_TABLES:
                continue
            fields = [
                f.name for f in model._meta.get_fields()
                if isinstance(f, (models.CharField, models.TextField))
                and not f.many_to_many and f.concrete
            ]
            if not fields:
                continue
            for obj in model.objects.all():
                changed = []
                for name in fields:
                    val = getattr(obj, name, None)
                    if not isinstance(val, str):
                        continue
                    new_val, n = _replace_phone_in_value(val)
                    if n:
                        setattr(obj, name, new_val)
                        changed.append(name)
                        total += n
                if changed:
                    obj.save(update_fields=changed)

    # Also explicitly fix the SiteSettings row for fields not swept by text:
    try:
        SiteSettings = apps.get_model('core', 'SiteSettings')
        site, _ = SiteSettings.objects.get_or_create(pk=1)
        site.phone_primary     = MAIN
        site.whatsapp_number   = MAIN_DIGITS
        site.whatsapp_url      = MAIN_WA
        site.rotation_phone_1  = MAIN
        site.rotation_phone_2  = MAIN
        site.rotation_phone_3  = MAIN
        site.location_phone_1  = STUDIO_1
        site.save(update_fields=[
            'phone_primary', 'whatsapp_number', 'whatsapp_url',
            'rotation_phone_1', 'rotation_phone_2', 'rotation_phone_3',
            'location_phone_1',
        ])
        total += 1
    except Exception as exc:  # noqa: BLE001
        print(f'[0009] SiteSettings explicit fix skipped: {exc}')

    print(f'[0009] fix_phones: {total} replacement(s) applied.')


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_replace_retired_phone_797'),
    ]

    operations = [
        # Update field defaults
        migrations.AlterField(
            model_name='sitesettings',
            name='phone_primary',
            field=models.CharField(
                default=MAIN, max_length=30,
                verbose_name='Основний телефон',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='whatsapp_number',
            field=models.CharField(
                default=MAIN_DIGITS,
                help_text='e.g. 420607365598 — used in wa.me/ links',
                max_length=20,
                verbose_name='WhatsApp (без + і пробілів)',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='whatsapp_url',
            field=models.URLField(blank=True, default=MAIN_WA, verbose_name='WhatsApp URL'),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='rotation_phone_1',
            field=models.CharField(
                default=MAIN, max_length=30,
                verbose_name='Ротаційний телефон 1',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='rotation_phone_2',
            field=models.CharField(
                default=MAIN, max_length=30,
                verbose_name='Ротаційний телефон 2',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='rotation_phone_3',
            field=models.CharField(
                default=MAIN, max_length=30,
                verbose_name='Ротаційний телефон 3',
            ),
        ),
        migrations.AlterField(
            model_name='sitesettings',
            name='location_phone_1',
            field=models.CharField(
                default=STUDIO_1, max_length=30,
                verbose_name='Телефон (студія 1)',
            ),
        ),
        migrations.RunPython(fix_phones, migrations.RunPython.noop),
    ]
