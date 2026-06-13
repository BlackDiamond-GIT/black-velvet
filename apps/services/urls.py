from django.urls import path

from . import views

app_name = 'services'

urlpatterns = [
    path('masaze/', views.ServiceListView.as_view(), name='list'),
    path('masaze/<slug:slug>/', views.ServiceDetailView.as_view(), name='detail'),
]
