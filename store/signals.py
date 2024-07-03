from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Product


@receiver(pre_save, sender=Product)
def new_price_default(sender, instance, **kwargs):
    if instance.off == 0:
        instance.new_price = instance.price


@receiver(pre_save, sender=Product)
def calculate_new_price(sender, instance, **kwargs):
    instance.new_price = instance.price - (instance.off * instance.price) / 100
