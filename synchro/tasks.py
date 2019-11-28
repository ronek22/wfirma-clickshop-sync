import requests

from django.conf import settings
from celery import task
from .models import City
from synchro.services.wfirma import WFirmaClient

import warnings
warnings.filterwarnings("ignore")

@task
def get_weather_data(city):
    api_key = settings.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={api_key}"
    data = requests.get(url).json()

    city, created = City.objects.update_or_create(name=city, defaults={
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'country': data['sys']['country'],
    })

@task
def get_wfirma_products():
    username, password = settings.WFIRMA_CRED
    client = WFirmaClient(username, password)
    client.get_goods()

