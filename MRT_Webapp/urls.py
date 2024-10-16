from django.urls import path, include 
from . import views 

urlpatterns = [
    path("", views.index, name='index'),
    path("sign_up/", views.sign_up, name='sign_up'),
    path("login/", views.login, name='login'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("logout/", views.logingOut, name="logout"),
    path("reservation_creation/", views.reservation_creation, name="reservation_creation"),
    path("payment_proceed/", views.payment_proceed, name="payment_proceed"),
    path("reservation_view/", views.reservation_view, name="reservation_view"),
    path("reservation_view/reservation_cancelled/<str:reservation_id>/", views.reservation_cancelled, name="reservation_cancelled"),
    path("paid/", views.paid, name="paid"),
    path("parking_manager/", views.parking_manager, name="parking_manager"),
    path("reservation_report/", views.reservation_report, name="reservation_report"),
    path("transaction/", views.transaction, name="transaction"),
]
