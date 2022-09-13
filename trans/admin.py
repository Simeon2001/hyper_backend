from django.contrib import admin
from .models import Transaction, DepositTrans

# Register your models here.
admin.site.register(Transaction)
admin.site.register(DepositTrans)
