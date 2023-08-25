from django.db import models
from django.utils import timezone
from datetime import datetime, date, time

# Create your models here.

class Account(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    joined_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email 
    

class Category(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name 

class CategoryItem(models.Model):
    class RecordType(models.TextChoices):
        EXISTENCE = '유무', 'existence'
        STRENGTH = '강도', 'strength'
        TIME = '시각', 'time'

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=10)
    created_date = models.DateTimeField(default=timezone.now)
    record_type = models.CharField(max_length=10 ,choices=RecordType.choices, default=RecordType.EXISTENCE)

    def __str__(self):
        return self.name 


class CategoryItemData(models.Model):
    category_item = models.ForeignKey(CategoryItem, on_delete=models.CASCADE)
    created_date = models.DateField(default=date.today)
    created_time = models.TimeField(default=datetime.now)

    figure = models.IntegerField(null=True)
    recorded_time = models.TimeField(null=True)
    
    def __str__(self):
        return self.category_item.name

class StatisticsResult(models.Model):
    content = models.TextField(max_length=200)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)


    
   

    
    