from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CompayUser(models.Model):
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE)

    country = models.CharField(max_length=20, blank=False, default="Nigeria")
    currency = models.CharField(max_length=10, blank=True, default="Naira")
    account_number = models.BigIntegerField(default=0)
    account_name = models.CharField(max_length=50, blank=False, default="CISCOQUAN")
    bank_name = models.CharField(max_length=20, blank=False, default="GTB")
    bitcoin_address = models.CharField(max_length=30, blank=True)
    mobile_number = models.BigIntegerField(default=0, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username) + "----" + str(self.country)

    @property
    def blank(self):
        if self.date_added == None:
            answer = True
            return answer
        else:
            answer = False
            return answer


class FiatWallet(models.Model):
    name = models.ForeignKey(
        CompayUser, on_delete=models.CASCADE, blank=False, related_name="names"
    )
    balance = models.BigIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name.user.username) + "----" + str(self.balance)


class UsdtWallet(models.Model):
    cname = models.ForeignKey(
        CompayUser, on_delete=models.CASCADE, blank=False, related_name="cnames"
    )
    balance = models.BigIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.cname.user.username) + "----" + str(self.balance)
