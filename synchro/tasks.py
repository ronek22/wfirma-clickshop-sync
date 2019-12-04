import requests

from django.conf import settings
from celery import task
from .models import City, Credentials, Shop, Product
from synchro.services.wfirma import WFirmaClient
from synchro.services.clickshop import ClickShopClient
from synchro.services.bot import Bot
import http.client
from datetime import datetime
import operator
from ratelimiter import RateLimiter

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
    credentials = Credentials.objects.all().first()
    username, password = credentials.login, credentials.password
    client = WFirmaClient(username, password)
    client.get_all_goods()

    rate_limiter = RateLimiter(max_calls=10, period=1)
    products_to_sync = Product.objects.all().filter(enabled=True)

    shops = Shop.objects.all()

    for shop in shops:
        click = ClickShopClient(shop)
        products_in_shop = click.get_all_products()
        products_variants = [x for x in products_in_shop if x.options]
        variants = []

        for product in products_variants:
            variants.extend(product.options)


        product_sync = [x for x in products_to_sync if x.code in [y.code for y in products_in_shop]]
        products_in_shop = [x for x in products_in_shop if x.code in [y.code for y in product_sync]]


        print(f"[DEBUG] Sklep: {len(products_in_shop)} | WFIRMA: {len(product_sync)}")
        keyfun = operator.attrgetter("code") 
        product_sync.sort(key=keyfun, reverse=True)
        products_in_shop.sort(key=keyfun, reverse=True)  

        pairs = list(zip(product_sync, products_in_shop))
        pairs = [(f,c) for f,c in pairs if int(f.available) != int(c.stock.stock)]

        for firma, clickshop in pairs:
            with rate_limiter:
                print(f"{firma.name} -> {clickshop.translations['pl_PL']['name']}")
                clickshop.stock.stock = int(firma.available)
                click.put_product(clickshop)

        # SELENIUM 
        bot = Bot(shop.url, shop.username, shop.password, products_to_sync)
        length = len(variants)
        for index, variant in enumerate(variants):
            print(f"[INFO] {index}/{length}")
            bot.edit_variant(variant)



    

