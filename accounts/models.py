from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fa = models.FloatField()
    kg = models.FloatField()
    edad = models.IntegerField()
    objetivo = models.CharField(max_length=100)
    def __str__(self):
        return f'Profile of {self.user.username}'
    

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    daily_calories = models.IntegerField()
    protein_percentage = models.FloatField()
    carbohydrate_percentage = models.FloatField()
    fat_percentage = models.FloatField()

class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    breakfast = models.CharField(max_length=100)
    lunch = models.CharField(max_length=100)
    dinner = models.CharField(max_length=100)

class Food(models.Model):
    index = models.IntegerField(primary_key=True, serialize=True)
    group = models.FloatField()
    energ_kal = models.FloatField()
    lipid_tot = models.FloatField()
    carbohydrt = models.FloatField()
    proteina = models.FloatField()
    name = models.CharField(max_length=1000)


    def __str__(self):
        return f"Food {self.index} - {self.energ_kal} kcal - {self.group} grupo - {self.lipid_tot} lipidos - {self.carbohydrt} carbohidratos - {self.proteina} proteina - Nombre:{self.name} "

class DailyIntake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    food = models.ManyToManyField(Food)
    calories = models.IntegerField()
    proteins = models.FloatField()
    carbohydrates = models.FloatField()
    fats = models.FloatField()

    def __str__(self):
        return f"{self.user.username} intake on {self.date}"