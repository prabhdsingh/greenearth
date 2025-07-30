from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

class EcoTag(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Plastic-Free", "Carbon Neutral"

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    vendor = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    eco_tags = models.ManyToManyField(EcoTag)
    is_organic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    eco_points = models.PositiveIntegerField(default=0)
