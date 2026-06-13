from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("out/", views.booking_out, name="booking_out"),
    path("whatsapp/", views.whatsapp_general, name="whatsapp_general"),
    path("whatsapp/<slug:slug>/", views.whatsapp_redirect, name="whatsapp_masseuse"),
]
