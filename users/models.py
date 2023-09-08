from datetime import datetime
from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    verification_code = models.CharField(max_length=6)
    attempts_remaining = models.PositiveIntegerField(default=3)
    verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=datetime.now)
    date_when_verified = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.name

    def save_data_joint(self):
        if self.verified and not self.date_when_verified:
            self.date_when_verified = datetime.now()

