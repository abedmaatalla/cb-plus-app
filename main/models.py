from django.db import models

# Create your models here.


class Product(models.Model):
    id = models.CharField(max_length=13, primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)


class Stock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    expired_at = models.DateField()

