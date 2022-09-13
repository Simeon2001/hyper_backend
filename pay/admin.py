from django.contrib import admin
from .models import CustomerInfo, PayLinks, MultiPay

# Register your models here.

admin.site.register(CustomerInfo)
admin.site.register(PayLinks)
admin.site.register(MultiPay)
