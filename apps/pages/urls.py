from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('cenik/', views.PricesView.as_view(), name='prices'),
    path('rozvrh/', views.ScheduleView.as_view(), name='schedule'),
    path('kontakt/', views.ContactView.as_view(), name='contact'),
    path('o-nas/', views.AboutView.as_view(), name='about'),
    path('pravidla-salonu/', views.SalonRulesView.as_view(), name='salon_rules'),
    path('zasady-ochrany/', views.PrivacyView.as_view(), name='privacy'),
]
