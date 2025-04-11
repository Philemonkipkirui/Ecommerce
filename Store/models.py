from django.db import models

# Create your models here.
from Accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Business user

    def __str__(self):
        return self.name 
    