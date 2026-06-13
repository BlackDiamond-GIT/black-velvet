from django.urls import path

from . import views

app_name = 'reservations'

urlpatterns = [
    path('rezervace/', views.ReservationWizardView.as_view(), name='wizard'),
    path('rezervace/krok/<int:step>/', views.WizardStepView.as_view(), name='step'),
    path('rezervace/potvrdit/', views.ConfirmReservationView.as_view(), name='confirm_submit'),
    path('rezervace/potvrdit/<uuid:token>/', views.ReservationConfirmView.as_view(), name='confirm'),
]
