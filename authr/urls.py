from django.urls import path
from authr import views
from authr.views import usercreateview


urlpatterns = [
    path("token", views.authrtoken, name="token/"),
    path("register", views.usercreateview, name="register/"),
    path("profile-status", views.p_status, name="status/"),
    path("search", views.user_searching, name="search/"),
    path("reset-password", views.reset_passwords, name="reset/"),
    path("verify-password", views.verify_token, name="reset/"),
]
