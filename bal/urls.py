from django.urls import path
from bal import views

urlpatterns = [
    path("bal", views.checker, name="balance/"),
    path("cbal", views.crypto_balance, name="balance/"),
    path("profile", views.profile, name="profile/"),
    path("create-profile", views.post_profilex, name="profile/"),
    path("notify", views.notification, name="notify/"),
]
