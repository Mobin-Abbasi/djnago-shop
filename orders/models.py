from django.db import models


# Create your models here.

class Order(models.Model):
    name = models.CharField(max_length=150)
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
        return sum(self.items.cost for item in self.items.all())