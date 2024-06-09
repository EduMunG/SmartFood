from django.db import models
from django.conf import settings

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fa = models.FloatField()
    kg = models.FloatField()
    edad = models.IntegerField()
    objetivo = models.CharField(max_length=100)
    def __str__(self):
        return f'Profile of {self.user.username}'