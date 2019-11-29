from django.contrib import admin
from .models import City, Product, Shop, Credentials

# Register your models here.
admin.site.register(City)
admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Credentials)