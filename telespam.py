from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pickle
import json

class TSpammer:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://web.telegram.org')
        self.storage = LocalStorage(self.driver)

    def store_to_file(self, filename="default.ws"):
        if self.storage != None:
            to_store = self.storage.getAll()
            fileObject = open(filename, 'wb')
            pickle.dump(to_store, fileObject)

    def load_from_file(self, filename="default.ws"):
        if self.storage != None:
            fileObject = open(filename,'rb')
            storedict = pickle.load(fileObject)
            self.storage.setAll(storedict)
            self.driver.refresh()

    def spam(self,contact,message,times):
        wait = WebDriverWait(self.driver,120)
        searchbox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ng-app"]/body/div[1]/div[2]/div/div[1]/div[1]/div/input')))
        searchbox.clear()
        searchbox.send_keys(contact + Keys.ENTER)
        textbox = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ng-app"]/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[2]/div/div/div/form/div[2]/div[5]')))
        for x in range(times):
            textbox.send_keys(message + Keys.ENTER)

class LocalStorage:

    def __init__(self, driver):
        self.driver = driver

    def set(self, key, value):
        self.driver.execute_script(
            "window.localStorage.setItem('{}',{})".format(key, json.dumps(value)))

    def get(self, key=None):
        if key:
            return self.driver.execute_script(
                "return window.localStorage.getItem('{}')".format(key))
        else:
            return self.driver.execute_script("""
                    var items = {}, ls = window.localStorage;
                    for (var i = 0, k; i < ls.length; i++)
                      items[k = ls.key(i)] = ls.getItem(k);
                    return items;
                    """)

    def remove(self, key):
        self.driver.execute_script(
            "window.localStorage.removeItem('{}');".format(key))

    def clear(self):
        self.driver.execute_script(
            "window.localStorage.clear();")

    def getAll(self):
        toReturn = {}
        for key, value in list(self.get().items()):
            toReturn[key] = value
        return toReturn

    def setAll(self, allKeys):
        for key, value in allKeys.items():
            self.set(key, value)
