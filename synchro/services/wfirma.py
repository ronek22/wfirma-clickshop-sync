import requests
from ..models import Product
import json

class WFirmaClient:
    """Client for consume api of wfirma
    Generally it will be one client in entire web app.
    """

    API = 'https://api2.wfirma.pl'

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def _get(self, endpoint, payload={'inputFormat':'json', 'outputFormat': 'json'}, data=None):
        response = requests.get(endpoint, params=payload, auth=(self.login, self.password), data=data)
        if response.status_code != 200:
            raise Exception(f"Problem with getting response, CODE: {response.status_code}")
        return response

    def get_goods(self, limit=100, page=1):
        filtered = {
            "goods": {
                "parameters": {
                    "limit": limit,
                    "page": page
                }
            }
        }
        response = self._get(f'{self.API}/goods/find', data=json.dumps(filtered))

        response = {x:y for x,y in response.json()['goods'].items() if x.isdigit()}
        if not response:
            return False
        for index, prod in response.items():
            product, created = Product.objects.update_or_create(
                name=prod['good']['name'],
                defaults = {
                    'code': prod['good']['code'],
                    'available': prod['good']['available'],
                    'modified': prod['good']['modified']
                }
            )
        return True

    def get_all_goods(self):
        page, products = 1, self.get_goods()
        while products:
            print(f"[DEBUG] WFIRMA Page: {page}")
            page+=1
            products = self.get_goods(page=page)
                


if __name__ == "__main__":
    client = WFirmaClient('ronekspotify@gmail.com', 'Wbmjmka96')
