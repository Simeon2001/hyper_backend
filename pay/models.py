from django.db import models
from bal.models import CompayUser

# Create your models here.
class PayLinks(models.Model):
    user = models.ForeignKey(CompayUser, blank=False, on_delete=models.CASCADE)
    reference = models.CharField(max_length=10, blank=False)
    access_no = models.CharField(max_length=16, blank=False, default="psj62bfdf5d4feb")
    id_no = models.IntegerField(default=0)
    success = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class CustomerInfo(models.Model):
    user = models.OneToOneField(CompayUser, blank=True, on_delete=models.CASCADE)
    customer_no = models.CharField(max_length=20, blank=True)
    recipient_code = models.CharField(max_length=20, blank=True)
    authorization_code = models.CharField(max_length=20, blank=True)
    subscription_code = models.CharField(max_length=20, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_no


class MultiPay(models.Model):
    title = models.CharField(max_length=100, blank=False)
    user = models.ForeignKey(
        CompayUser, blank=False, on_delete=models.CASCADE, related_name="Giver"
    )
    pay_user = models.ManyToManyField(CompayUser, blank=True, related_name="Collector")
    closing_no = models.IntegerField(default=0)
    access_no = models.CharField(max_length=10, blank=False, default="abc5580939")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
