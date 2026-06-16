from django.templatetags.static import static
from django.urls import reverse_lazy


UNFOLD = {
    'SITE_TITLE': 'Black Velvet Admin',
    'SITE_HEADER': 'Black Velvet Spa',
    'SITE_SUBHEADER': 'Керування контентом',
    'SITE_URL': '/',
    'SITE_ICON': lambda request: static('img/favicon.svg'),
    'SITE_LOGO': lambda request: static('img/favicon.svg'),
    'SITE_FAVICONS': [
        {
            'rel': 'icon',
            'type': 'image/svg+xml',
            'href': lambda request: static('img/favicon.svg'),
        },
        {
            'rel': 'icon',
            'type': 'image/png',
            'sizes': '180x180',
            'href': lambda request: static('img/favicon.png'),
        },
        {
            'rel': 'apple-touch-icon',
            'href': lambda request: static('img/favicon.png'),
        },
    ],
    'SITE_SYMBOL': 'spa',
    'THEME': 'dark',
    'SHOW_HISTORY': True,
    'SHOW_VIEW_ON_SITE': True,
    'STYLES': [
        lambda request: static('css/admin-header.css?v=2'),
    ],
    'COLORS': {
        'primary': {
            '50': 'oklch(97% 0.02 25)',
            '100': 'oklch(94% 0.04 25)',
            '200': 'oklch(88% 0.08 25)',
            '300': 'oklch(78% 0.14 25)',
            '400': 'oklch(65% 0.18 25)',
            '500': 'oklch(55% 0.20 25)',
            '600': 'oklch(48% 0.19 25)',
            '700': 'oklch(42% 0.17 25)',
            '800': 'oklch(35% 0.14 25)',
            '900': 'oklch(28% 0.11 25)',
            '950': 'oklch(20% 0.08 25)',
        },
        'base': {
            '50': 'oklch(98% 0.01 280)',
            '100': 'oklch(95% 0.01 280)',
            '200': 'oklch(90% 0.01 280)',
            '300': 'oklch(82% 0.01 280)',
            '400': 'oklch(70% 0.01 280)',
            '500': 'oklch(58% 0.01 280)',
            '600': 'oklch(48% 0.01 280)',
            '700': 'oklch(38% 0.01 280)',
            '800': 'oklch(22% 0.015 280)',
            '900': 'oklch(14% 0.015 280)',
            '950': 'oklch(9% 0.01 280)',
        },
    },
    'EXTENSIONS': {
        'modeltranslation': {
            'flags': {
                'cs': '🇨🇿',
                'en': '🇬🇧',
                'ru': '🇷🇺',
            },
        },
    },
    'SIDEBAR': {
        'show_search': True,
        'show_all_applications': False,
        'navigation': [
            {
                'title': 'Огляд',
                'separator': True,
                'items': [
                    {
                        'title': 'Панель',
                        'icon': 'dashboard',
                        'link': reverse_lazy('admin:index'),
                    },
                ],
            },
            {
                'title': 'Налаштування',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Налаштування сайту',
                        'icon': 'settings',
                        'link': reverse_lazy('admin:core_sitesettings_changelist'),
                    },
                    {
                        'title': 'Редиректи',
                        'icon': 'sync_alt',
                        'link': reverse_lazy('admin:core_legacyredirect_changelist'),
                    },
                ],
            },
            {
                'title': 'Контент',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Сторінки',
                        'icon': 'description',
                        'link': reverse_lazy('admin:core_contentpage_changelist'),
                    },
                    {
                        'title': 'Відгуки гостей',
                        'icon': 'reviews',
                        'link': reverse_lazy('admin:core_guestreview_changelist'),
                    },
                ],
            },
            {
                'title': 'Масажистки',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Масажистки',
                        'icon': 'groups',
                        'link': reverse_lazy('admin:team_masseuse_changelist'),
                    },
                    {
                        'title': 'Бібліотека фото',
                        'icon': 'collections',
                        'link': reverse_lazy('admin:media_library_cloudinaryimage_changelist'),
                    },
                    {
                        'title': 'Розклад',
                        'icon': 'schedule',
                        'link': reverse_lazy('admin:reservations_timeslot_changelist'),
                    },
                    {
                        'title': 'Тижневі зміни',
                        'icon': 'calendar_month',
                        'link': reverse_lazy('admin:pages_masseuseshift_changelist'),
                    },
                ],
            },
            {
                'title': 'Послуги',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Послуги',
                        'icon': 'spa',
                        'link': reverse_lazy('admin:services_service_changelist'),
                    },
                ],
            },
            {
                'title': 'Бронювання',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Кліки',
                        'icon': 'ads_click',
                        'link': reverse_lazy('admin:booking_bookingclick_changelist'),
                    },
                    {
                        'title': 'WhatsApp шаблони',
                        'icon': 'chat',
                        'link': reverse_lazy('admin:booking_whatsapptemplate_changelist'),
                    },
                    {
                        'title': 'Резервації',
                        'icon': 'event_available',
                        'link': reverse_lazy('admin:reservations_reservation_changelist'),
                    },
                ],
            },
            {
                'title': 'Блог',
                'collapsible': True,
                'items': [
                    {
                        'title': 'Статті',
                        'icon': 'article',
                        'link': reverse_lazy('admin:blog_post_changelist'),
                    },
                    {
                        'title': 'Теги',
                        'icon': 'label',
                        'link': reverse_lazy('admin:blog_tag_changelist'),
                    },
                ],
            },
            {
                'title': 'Сторінки сайту',
                'collapsible': True,
                'items': [
                    {
                        'title': 'FAQ',
                        'icon': 'help',
                        'link': reverse_lazy('admin:pages_faq_changelist'),
                    },
                    {
                        'title': 'Відгуки',
                        'icon': 'star',
                        'link': reverse_lazy('admin:pages_review_changelist'),
                    },
                    {
                        'title': 'Прайс',
                        'icon': 'payments',
                        'link': reverse_lazy('admin:pages_pricecategory_changelist'),
                    },
                    {
                        'title': 'Повідомлення',
                        'icon': 'mail',
                        'link': reverse_lazy('admin:pages_contactmessage_changelist'),
                    },
                ],
            },
        ],
    },
}
