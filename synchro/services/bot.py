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
        self.driver = webdriver.Remote(command_executor=f'http://hub:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)
        self.url = f"{url}/admin/"
        self.login = login
        self.password = password
        self.productsList = productsList
        self.ignoredExceptions = (StaleElementReferenceException,)
        self.wait = WebDriverWait(self.driver, 60, ignored_exceptions=self.ignoredExceptions)
        self.quickWait = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignoredExceptions)
        self._login()

    def _login(self):
        self.driver.get(self.url)

        current = self.driver.current_url
        
        username = self.wait.until(ec.visibility_of_element_located((By.NAME, 'login'))).send_keys(self.login)
        password = self.wait.until(ec.visibility_of_element_located((By.NAME, 'password')))
        password.send_keys(self.password)
        password.submit()
        
        self.quickWait.until(ec.url_changes(current))


    def edit_variant(self, id):
        endpoint = f"{self.url}products/editoption/id/{id}/stock/1"
        self.driver.get(endpoint)
        code = self.wait.until(ec.visibility_of_element_located((By.NAME, 'code')))
        try:
            code = code.get_attribute('value')
        except StaleElementReferenceException:
            code = self.wait.until(ec.visibility_of_element_located((By.NAME, 'code')))
            code = code.get_attribute('value')

        if code:
            corresponding = next((x for x in self.productsList if x.code == code), None)
            
            if corresponding:
                print(f"[DEBUG] ID: {id} CODE: {corresponding.code} FOUND CORRESPONDING FOR: {corresponding.name} -> {corresponding.available}")
                value = int(corresponding.available)
                stan = self.wait.until(ec.visibility_of_element_located((By.NAME, 'optstock')))
                stan.clear(); stan.send_keys(value)
                self.wait.until(lambda browser: stan.get_attribute('value') == str(value))

                save_button = self.wait.until(ec.visibility_of_element_located((By.NAME, 'savenquit'))).click()

                self.quickWait.until(ec.url_changes(endpoint))



    def close(self):
        self.driver.quit()


# if __name__ == "__main__":
#     bot = Bot('http://hurt.gardenplus.eu/admin/')

