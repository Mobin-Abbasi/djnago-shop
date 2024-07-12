from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.

@admin.register(ShopUser)
class ShopUserAdmin(UserAdmin):
    ordering = ['phone']
    list_display = ['phone', 'first_name', 'last_name', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        (None,
         {'fields': ('address', )}),
    )