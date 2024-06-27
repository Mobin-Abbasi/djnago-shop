from django.db import models


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=155)
    slug = models.SlugField(max_length=155, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name


class ProductFeature(models.Model):
    name = models.CharField(max_length=155)
    value = models.CharField(max_length=155)

    def __str__(self):
        return f"{self.name}: {self.value}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=155)
    description = models.TextField()
    slug = models.SlugField(max_length=155)
    inventory = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)
    off = models.PositiveIntegerField(default=0)
    new_price = models.PositiveIntegerField(default=0)
    feature = models.ForeignKey(ProductFeature, on_delete=models.CASCADE, related_name="features")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.name


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    file = models.ImageField(upload_to='product_images/%Y/%m/%d')
    title = models.CharField(max_length=155)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.title