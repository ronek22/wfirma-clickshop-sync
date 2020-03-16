from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import exceptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException
import os
import socket
from retry import retry

DEBUG = False

class Bot:
    def __init__(self, url, login, password, productsList):
        """productsList from WFIRMA"""
        # if not DEBUG:
        #     options = webdriver.ChromeOptions()
        #     options.add_argument("--headless")
        #     self.driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
        # else:
        #     self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Remote(command_executor=f'http://hub:4444/wd/hub',
        desired_capabilities=options.to_capabilities())
        self.url = f"{url}/admin/"
        self.login = login
        self.password = password
        self.productsList = productsList
        self.ignoredExceptions = (StaleElementReferenceException,)
        self.wait = WebDriverWait(self.driver, 120, ignored_exceptions=self.ignoredExceptions)
        self.quickWait = WebDriverWait(self.driver, 30, ignored_exceptions=self.ignoredExceptions)
        self._login()

    def _login(self):
        self.driver.get(self.url)

        current = self.driver.current_url
        
        username = self.wait.until(ec.visibility_of_element_located((By.NAME, 'login'))).send_keys(self.login)
        password = self.wait.until(ec.visibility_of_element_located((By.NAME, 'password')))
        password.send_keys(self.password)
        password.submit()
        
        self.quickWait.until(ec.url_changes(current))

    @retry(StaleElementReferenceException, tries=3, delay=1)
    def _get_data(self, local):
        data = self.wait.until(ec.visibility_of_element_located(local))
        return data.get_attribute('value')

    @retry(StaleElementReferenceException, tries=3, delay=1)
    def _fill_data(self, local, value):
        data = self.wait.until(ec.visibility_of_element_located(local))
        data.clear()
        data.send_keys(value)
        return data


    def edit_variant(self, id):
        endpoint = f"{self.url}products/editoption/id/{id}/stock/1"
        self.driver.get(endpoint)

        code = self._get_data((By.NAME, 'code'))

        if code:
            corresponding = next((x for x in self.productsList if x.code == code), None)
            
            if corresponding:
                print(f"[DEBUG] ID: {id} CODE: {corresponding.code} FOUND CORRESPONDING FOR: {corresponding.name} -> {corresponding.available}")
                value = int(corresponding.available)
                stan = self._fill_data((By.NAME, 'optstock'), value)
                self.wait.until(lambda browser: stan.get_attribute('value') == str(value))

                save_button = self.wait.until(ec.visibility_of_element_located((By.NAME, 'savenquit'))).click()

                self.quickWait.until(ec.url_changes(endpoint))



    def close(self):
        self.driver.quit()


# if __name__ == "__main__":
#     bot = Bot('http://hurt.gardenplus.eu/admin/')

