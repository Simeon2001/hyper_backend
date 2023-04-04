from django.urls import path
from trans import views

urlpatterns = [
    path("trans", views.api_algo, name="apitrans/"),
    path("mtrans/<str:access>", views.multipay_algo, name="apitrans/"),
]
