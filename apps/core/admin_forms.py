from django.conf import settings
from tinymce.widgets import AdminTinyMCE

RICH_TEXT_WIDGET = AdminTinyMCE(
    attrs={
        'cols': 80,
        'rows': 25,
    },
)


def rich_text_widgets(*field_names):
    widgets = {}
    for name in field_names:
        widgets[name] = RICH_TEXT_WIDGET
        for lang_code, _ in settings.LANGUAGES:
            widgets[f'{name}_{lang_code}'] = RICH_TEXT_WIDGET
    return widgets
