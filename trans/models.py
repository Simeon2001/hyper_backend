from django.db import models
from bal.models import FiatWallet, UsdtWallet, CompayUser

# Create your models here.
class Transaction(models.Model):
    amount = models.IntegerField(default=0)
    send = models.ForeignKey(
        FiatWallet, on_delete=models.CASCADE, blank=False, related_name="sending"
    )
    receive = models.ForeignKey(
        FiatWallet, on_delete=models.CASCADE, blank=False, related_name="receiving"
    )
    date_added = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(max_length=30, default="payment", blank=True)

    def __str__(self):
        return (
            str(self.amount)
            + " from "
            + str(self.send.name.user.username)
            + " to "
            + str(self.receive.name.user.username)
            + " for "
            + str(self.reason)
        )


class DepositTrans(models.Model):
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(CompayUser, blank=False, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount) + " deposited " + " on " + str(self.date_added)
