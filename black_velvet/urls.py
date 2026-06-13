from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.i18n import set_language

from apps.core.views import robots_txt, toggle_admin_language
from black_velvet.sitemaps import SITEMAPS

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/media-library/', include('apps.media_library.urls')),
    path('admin/toggle-lang/', toggle_admin_language, name='admin_toggle_lang'),
    path('tinymce/', include('tinymce.urls')),
    path('booking/', include('apps.booking.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='sitemap'),
    path('robots.txt', robots_txt, name='robots'),
    path('i18n/setlang/', set_language, name='set_language'),
]

urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    path('', include('apps.services.urls')),
    path('', include('apps.team.urls')),
    path('', include('apps.reservations.urls')),
    path('', include('apps.blog.urls')),
    path('', include('apps.pages.urls')),
    prefix_default_language=False,
)

if settings.DEBUG or settings.SERVE_MEDIA:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'
