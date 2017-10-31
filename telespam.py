from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pickle
import json

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
