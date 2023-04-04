from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ResetToken(models.Model):
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    token = models.IntegerField(blank=False)

    def __str__(self):
        return self.user.username
