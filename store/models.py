from django.db import models

# Create your models here.
# data is created in objects, called Models, and is actually tables in a database.

class Customer (models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Product (models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Order (models.Model):
    invoice = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField()

    def __str__(self):
        return self.invoice