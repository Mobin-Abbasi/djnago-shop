from django.db import models

from store.models import Product
from account.models import ShopUser


# Create your models here.

class Order(models.Model):
    buyer = models.ForeignKey(ShopUser, related_name='orders', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'Order #{self.id}'

    def get_total_cost(self):
        return sum(item.get_costs() for item in self.items.all())

    def get_post_cost(self):
        weight = sum(item.get_weight() for item in self.items.all())
        if weight < 1000:
            return 20000
        elif 1000 < weight < 2000:
            return 30000
        else:
            return 50000

    def get_final_cost(self):
        return self.get_total_cost() + self.get_post_cost()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=1)
    weight = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)

    def get_costs(self):
        return self.price * self.quantity

    def get_weight(self):
        return self.weight * self.quantity
