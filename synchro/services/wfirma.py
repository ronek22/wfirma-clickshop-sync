import requests
from ..models import Product

class WFirmaClient:
    """Client for consume api of wfirma
    Generally it will be one client in entire web app.
    """

    API = 'https://api2.wfirma.pl'

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def _get(self, endpoint, payload={'outputFormat': 'json'}):
        response = requests.get(endpoint, params=payload, auth=(self.login, self.password))
        if response.status_code != 200:
            print(f"Problem with getting response, CODE: {response.status_code}")
            return False
        return response

    def get_goods(self, limit=20, page=1):
        response = self._get(f'{self.API}/goods/find')
        if response:
            response = {x:y for x,y in response.json()['goods'].items() if x.isdigit()}
            for index, prod in response.items():
                product, created = Product.objects.update_or_create(
                    name=prod['good']['name'],
                    defaults = {
                        'code': prod['good']['code'],
                        'available': prod['good']['available'],
                        'modified': prod['good']['modified']
                    }
                )
                


if __name__ == "__main__":
    client = WFirmaClient('ronekspotify@gmail.com', 'Wbmjmka96')
