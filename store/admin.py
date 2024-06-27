from django.contrib import admin
from .models import *


# Register your models here.


class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


class FeatureInline(admin.StackedInline):
    model = ProductFeature
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'slug']
    search_fields = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'inventory', 'new_price', 'created']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['created', 'updated', 'off']
    search_fields = ['name', 'description', 'inventory', 'off']
    inlines = [ImageInline, FeatureInline]