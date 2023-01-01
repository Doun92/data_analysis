from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import pandas as pd


class Scrap_Pokepedia:
    # On appelle les variables par défaut
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Firefox()

    def test(self):
        print(self.url)
