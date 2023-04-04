from django.urls import path
from pay import views

urlpatterns = [
    path("link", views.generate, name="apitrans/"),
    path("customer", views.create_customer, name="apitrans/"),
    path("nuban", views.generate_nuban, name="apitrans/"),
    path("multi-info", views.multi_payinfo, name="apitrans/"),
    path("multi-post/<str:pk>", views.multi_post, name="apitrans/"),
]
