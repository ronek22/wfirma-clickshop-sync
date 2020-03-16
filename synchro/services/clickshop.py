import requests
from .models import Token, ClickProduct
from ..models import Shop
from pathlib import Path
from datetime import datetime, timedelta
from time import sleep
import warnings
warnings.filterwarnings("ignore")


class ClickShopClient:

    def __init__(self, shop: Shop):
        self.shop = shop
        self.url = f"{shop.url}/webapi/rest"
        self.username = shop.username
        self.password = shop.password
        self.token = self.get_token()
        self.max_page = None


    #region Authentication
    def get_token(self):
        token = self.shop.access_token
        if not token:
            token = self._get_token()
        elif self.shop.expires_in.replace(tzinfo=None) < datetime.now().replace(tzinfo=None):
            token = self._get_token()

        return token
    

    def _get_token(self):
        response = requests.post(
                f'{self.url}/auth',
                auth=(self.username, self.password)
            )
        token = Token.from_json(response.content)
        # update Shop object
        self.shop.access_token = token.access_token
        self.shop.expires_in = token.expiration_date
        self.shop.save()

        return self.shop.access_token
    #endregion

    def get_products(self, page=1):
        '''Returns 50 products per page'''
        payload={'page': page, 'limit': 50}
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(f"{self.url}/products", headers=headers, params=payload)
        if response.status_code != 200:
            # raise Exception(f"Problem with API: {response.status_code}")
            print("[INFO] Getting 429, wait 10s and continue...")
            sleep(10)
            return self.get_products(page)
        response = response.json()
        if page == 1:
            self.max_page = response['pages']
        products = [ClickProduct.from_dict(x) for x in response['list']]
        return products
    
    def get_all_products(self):
        products = []
        products.extend(self.get_products())

        for page in range(2, self.max_page+1):
            print(f"[DEBUG] Page: {page}")
            products.extend(self.get_products(page=page))
        
        return products
    
    def put_product(self, product: ClickProduct):
        headers = {'Authorization': f'Bearer {self.token}'}
        payload = product.to_json()
        response = requests.put(f"{self.url}/products/{product.product_id}", data=product.to_json(), headers=headers)
        print(f"STATUS OF UPDATE: {response.status_code}")
        if response.status_code == 429:
            print("="*20)
            print(f"PROBLEM: {response.content}")
            print("-"*20)
            print(f"HEADERS: {response.headers}")
            sleep(1)
            print("RETRY")
            return self.put_product(product)
        elif response.status_code != 200:
            print("="*20)
            print(f"PROBLEM: {response.content}")
            print("-"*20)
            print(f"HEADERS: {response.headers}")
            print(f"Product options: {product.to_json()}") # test





if __name__ == "__main__":
    client = ClickShopClient('http://hurt.gardenplus.eu',
    'j.ronkiewicz', 'Jakub123')