import requests

from django.conf import settings
from celery import task
from .models import City
from synchro.services.wfirma import WFirmaClient
import http.client
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")


@task
def get_wfirma_products():
    username, password = settings.WFIRMA_CRED
    client = WFirmaClient(username, password)
    client.get_goods()

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

