from django.urls import path

from . import views

app_name = 'team'

urlpatterns = [
    path('maserky/', views.TeamListView.as_view(), name='list'),
    path('maserky/<slug:slug>/', views.MasseuseDetailView.as_view(), name='detail'),
]
