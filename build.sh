#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py migrate --no-input
python3 <<'PY' 2>/dev/null || true
from pathlib import Path
from babel.messages.pofile import read_po
from babel.messages.mofile import write_mo
po_path = Path('locale/uk/LC_MESSAGES/django.po')
with po_path.open('r', encoding='utf-8') as f:
    catalog = read_po(f, locale='uk')
with Path('locale/uk/LC_MESSAGES/django.mo').open('wb') as f:
    write_mo(f, catalog)
PY
python manage.py create_admin_user
python manage.py seed_data
python manage.py collectstatic --no-input
