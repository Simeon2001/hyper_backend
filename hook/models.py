from django.db import models

# Create your models here.
class PayPlan(models.Model):
    plan_name = models.CharField(max_length=30, blank=False)
    plan_code = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return self.plan_name
