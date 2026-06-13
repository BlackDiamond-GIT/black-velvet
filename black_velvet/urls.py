from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.i18n import set_language

from apps.core.views import robots_txt
from black_velvet.sitemaps import SITEMAPS

urlpatterns = [
    path('admin/', admin.site.urls),
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
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.core.views.handler404'
handler500 = 'apps.core.views.handler500'
