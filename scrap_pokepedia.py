# Imports
from pathlib import Path
import Web_Scrapping_Tool

# Data
data_folder = Path("datasets/")

dataset_to_fill = f"{data_folder}/pokedex.csv"

csv_file =  open(dataset_to_fill, "r", encoding="utf-8")

# On cherche quel a été le pokemon traité en dernier
final_line = csv_file.readlines()[-1]
pkm_now = final_line.split(',')

print(pkm_now[2])

# On reprend au dernier pokemon de la liste, sauf si la liste est vide, là, on commence à Bulbizare
if pkm_now[2] == 'nom_fr':
    pokemon = 'Bulbizare'
else:
    pokemon = pkm_now[3]
    # Pour enlever les guillemets héritées de la csv
    pokemon = pokemon[1:-1:]

url = f"https://www.pokepedia.fr/{pokemon}"
scrapper = Web_Scrapping_Tool.Scrap_Pokepedia(url=url)

test = scrapper.test()
