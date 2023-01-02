# Imports
from pathlib import Path
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import Web_Scrapping_Tool

# Data
data_folder = Path("datasets/")

dataset_to_fill = f"{data_folder}/pokedex.csv"

driver = webdriver.Firefox()

continue_scrp = True

pokemon = "Pandarbare"

scrapper = Web_Scrapping_Tool.Scrap_Pokepedia(pokemon=pokemon, driver=driver)

while continue_scrp:
    # On reprend au dernier pokemon de la liste, sauf si la liste est vide, là, on commence à Bulbizare
    get_number = scrapper.get_number()
    get_names = scrapper.get_names(pokemon)
    get_types = scrapper.get_types(pokemon)
    get_stats = scrapper.get_stats()
    get_divers = scrapper.get_divers(pokemon)
    get_numbers = scrapper.get_pkdex_nb()

    dict_file = open("dict_file.txt", "w", encoding="utf8")
    dict_file.write(str(get_numbers))
    # dict_file.close()

    # print(get_numbers)
    # with open(dataset_to_fill, 'a', newline='', encoding="utf8") as csv_file:
    #     # Créez un objet writer CSV
    #     writer = csv.writer(csv_file)
    #     writer.writerow(get_numbers.keys())
    #     writer.writerow(get_numbers.values())
    # csv_file.close()
    # Click on next pokemon
    elem = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[1]/td[9]/a'))
    )
    elem.click()