from django.contrib import admin
from .models import CompayUser, FiatWallet, UsdtWallet

# Register your models here.

admin.site.register(CompayUser)
admin.site.register(FiatWallet)
admin.site.register(UsdtWallet)
