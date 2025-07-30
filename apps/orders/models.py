from django.db import models

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('cancelled', 'Cancelled'), ('delivered', 'Delivered')], default='delivered')
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[('cancelled', 'Cancelled'), ('delivered', 'Delivered')], default='delivered')

    def __str__(self):
        return self.product.name
