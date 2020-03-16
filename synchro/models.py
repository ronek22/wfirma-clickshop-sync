from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError

class City(models.Model):
    name = models.CharField(max_length=64, unique=True)
    temperature = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    icon = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=300, unique=False)
    code = models.CharField(max_length=50, unique=True)
    available = models.FloatField()
    modified = models.DateTimeField(null=True, blank=True)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} | {self.code}"

class Shop(models.Model):
    url = models.URLField()
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    access_token = models.CharField(max_length=200, null=True)
    expires_in = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse("shop-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.url

class Credentials(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=40)

    def get_absolute_url(self):
        return reverse("credentials", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.pk and Credentials.objects.exists():
            raise ValidationError('There is can be only one Credential in entire site')
        return super(Credentials, self).save(*args, **kwargs) 
    
    def __str__(self):
        return self.login

    