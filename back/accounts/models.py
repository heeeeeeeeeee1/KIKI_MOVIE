from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', '남성'),
        ('W', '여성'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    birth_date = models.DateField(null=True)
    introduce = models.TextField(null=True)

    def __str__(self):
        return self.username