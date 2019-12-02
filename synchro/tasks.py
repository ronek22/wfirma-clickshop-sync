import requests

from django.conf import settings
from celery import task
from .models import City, Credentials, Shop, Product
from synchro.services.wfirma import WFirmaClient
from synchro.services.clickshop import ClickShopClient
import http.client
from datetime import datetime
import operator

import warnings
warnings.filterwarnings("ignore")


@task
def get_wfirma_products():
    credentials = Credentials.objects.all().first()
    username, password = credentials.login, credentials.password
    client = WFirmaClient(username, password)
    client.get_all_goods()

@task
def send_discord_message():
        webhookurl = "https://discordapp.com/api/webhooks/613400548120592398/tNUJUq-7ntfEEx2Ai6aEDWN-ahMsSD_qJCnapfUUXVBvxa2_0WdOQyJIp6SnYsjWY0Aa"
        formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n" + "TESTUJEMY PERIODIC TASK" + datetime.now().strftime("%H:%M:%S") + "\r\n------:::BOUNDARY:::--"
        connection = http.client.HTTPSConnection("discordapp.com")
        connection.request("POST", webhookurl, formdata, {
            'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
            'cache-control': "no-cache",
            })
        response = connection.getresponse()
        result = response.read()
        return result.decode("utf-8")

@task
def authenticate_shop():
    credentials = Shop.objects.all()
    for cred in credentials:
        client = ClickShopClient(cred)

@task
def synchronize():
    # update wfirma database
    # credentials = Credentials.objects.all().first()
    # username, password = credentials.login, credentials.password
    # client = WFirmaClient(username, password)
    # client.get_all_goods()

    products_to_sync = Product.objects.all().filter(enabled=True)

    shops = Shop.objects.all()

    for shop in shops:
        click = ClickShopClient(shop)
        products_in_shop = click.get_all_products()

        product_sync = [x for x in products_to_sync if x.code in [y.code for y in products_in_shop]]
        products_in_shop = [x for x in products_in_shop if x.code in [y.code for y in product_sync]]

        print(f"[DEBUG] Sklep: {len(products_in_shop)} | WFIRMA: {len(product_sync)}")
        keyfun = operator.attrgetter("code") 
        product_sync.sort(key=keyfun, reverse=True)
        products_in_shop.sort(key=keyfun, reverse=True)  

        for firma,clickshop in zip(product_sync, products_in_shop):
            print(f"{firma.name} -> {clickshop.translations['pl_PL']['name']}")
            # print(f"{firma.code} -> {clickshop.code}")
            if int(firma.available) != int(clickshop.stock.stock):
                print(f"[UPDATE] Different stock: {int(firma.available)} != {int(clickshop.stock.stock)}")
                clickshop.stock.stock = int(firma.available)
                click.put_product(clickshop)

    

