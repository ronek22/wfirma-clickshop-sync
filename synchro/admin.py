from django.contrib import admin
from .models import City, Product, Shop, Credentials

# Register your models here.
admin.site.register(Product)
admin.site.register(Shop)