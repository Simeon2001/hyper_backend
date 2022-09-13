from django.urls import path
from hook import views

urlpatterns = [
    path("webhook", views.pay_hook, name="hook/"),
]
