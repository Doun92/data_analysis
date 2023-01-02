from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from html.parser import HTMLParser
import re

class Scrap_Pokepedia:
    # On appelle les variables par défaut
    def __init__(self, pokemon, driver):
        self.url = f"https://www.pokepedia.fr/{pokemon}"
        self.driver = driver
        self.dict_to_csv = {}
        self.driver.get(self.url)

    def get_number(self):
        # Numéro du pokemon
        xpath_number = self.driver.find_element(
        By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/thead/tr/th[1]/big/span')
        number = xpath_number.get_attribute('innerHTML')[-3:]
        self.dict_to_csv["numero_pkm"] = number
        number_int = int(number)
        if number_int <= 151:
            self.dict_to_csv['génération'] = 1
        elif number_int >= 152 <= 251:
            self.dict_to_csv['génération'] = 2
        elif number_int >= 252 <= 386:
            self.dict_to_csv['génération'] = 3
        elif number_int >= 387 <= 494:
            self.dict_to_csv['génération'] = 4
        elif number_int >= 495 <= 649:
            self.dict_to_csv['génération'] = 5
        elif number_int >= 650 <= 721:
            self.dict_to_csv['génération'] = 6
        elif number_int >= 722 <= 808:
            self.dict_to_csv['génération'] = 7
        elif number_int >= 809 <= 904:
            self.dict_to_csv['génération'] = 8
        elif number_int >= 809 <= 904:
            self.dict_to_csv['génération'] = 8

        # print(self.dict_to_csv)
        return(self.dict_to_csv)

    def get_names(self, pkm):
        if pkm in ["Magnéti", "Ectoplasma", "Smogo", "Tarinor", "Magnézone", "Giratina", "Shaymin", "Amphinobi", "Pandespiègle"]:
            xpath_li_names = self.driver.find_element(
                By.XPATH,
                '/html/body/div[3]/div[3]/div[5]/div[1]/ul[3]')
        elif pkm in ["Canarticho", "Onix", "Rhinocorne", "Aquali", "Qulbutoké", "Skitty", "Kecleon", "Cheniselle", "Coudlangue", "Noctunoir", "Motisma", "Cresselia", "Sapereau", "Pandarbare"]:
            xpath_li_names = self.driver.find_element(
                By.XPATH,
                '/html/body/div[3]/div[3]/div[5]/div[1]/ul[2]')
        elif pkm in ["Évoli", "Zarbi", "Morphéo", "Cheniti"]:
            xpath_li_names = self.driver.find_element(
                By.XPATH,
                '/html/body/div[3]/div[3]/div[5]/div[1]/ul[4]')
        elif pkm in ["Tarinorme"]:
            xpath_li_names = self.driver.find_element(
                By.XPATH,
                '/html/body/div[3]/div[3]/div[5]/div[1]/ul[3]')
        else:
        # Find the list with all names
            xpath_li_names = self.driver.find_element(
            By.XPATH, 
            '/html/body/div[3]/div[3]/div[5]/div[1]/ul[2]')
        # print(xpath_li_names)
        inner_li_names = xpath_li_names.get_attribute('innerHTML')
        soup = BeautifulSoup(inner_li_names, 'html.parser')
        # print(soup)
        all_li = soup.findAll('li')
        # print(all_li)
        for li in all_li:
            # print(li)
            txt = str(li)
            # print(txt)
            text_list = txt.split("<i>")
            # print(text_list)
            langue = text_list[0][4:]
            langue_inter = langue.split("\xa0:")[0]
            # print(langue_inter)
            nom = text_list[1].split("</i>")[0]
            # print(nom)
            if langue_inter in ["Français", "Anglais", "Allemand", "Japonais"]:
                self.dict_to_csv[langue_inter] = nom
        return self.dict_to_csv

    def get_types(self, pkm):
        if pkm in ["Morphéo", "Cheniselle", "Motisma", "Shaymin", "Darumacho", "Meloetta"]:
            no_type = " "
            self.dict_to_csv["Type_" + str(no_type)] = "A faire à la main"
        else:
            xpath_types = self.driver.find_element(
                By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[8]/td'
            )
            inner_types = xpath_types.get_attribute('innerHTML')
            soup = BeautifulSoup(inner_types, 'html.parser')
            all_a_ty = soup.findAll('a')
            # print(len(all_a_ty))
            no_type = 1
            for a in all_a_ty:
                type = a.get('title')
                type = type.split(" ")[0]
                self.dict_to_csv["Type_" + str(no_type)] = type
                no_type += 1

        return self.dict_to_csv

    def get_stats(self):
        page = self.driver.find_element(
            By.ID, "mw-content-text")
        inner_page = page.get_attribute('innerHTML')
        soup = BeautifulSoup(inner_page, 'html.parser')
        # print(soup)
        soup_str = str(soup)
        after_stats_id = soup_str.split('id="Statistiques"')
        list_tr = after_stats_id[1].split('<tr>')

        # Regex
        regex_search_stats = r'>\d{2,3}'
        regex_search_nom = r'(#\w+)|(Somme des statistiques de base)'

        pv = list_tr[4]
        atk = list_tr[5]
        defense = list_tr[6]
        atk_spé = list_tr[7]
        def_spé = list_tr[8]
        vitesse = list_tr[9]
        spécial = list_tr[10]
        somme = list_tr[11]
        # print(somme)

        list_stats = [pv, atk, defense, atk_spé, def_spé, vitesse, spécial, somme]

        for item in list_stats:
            try:
                get_stat = re.search(regex_search_stats, item)
                # print(get_stat.group()[1:])
                statistique = get_stat.group()[1:]
                # print(statistique)
            except:
                pass

            try:
                get_noms = re.search(regex_search_nom, item)
                if get_noms.group() == "Somme des statistiques de base":
                    noms_stats = get_noms.group()
                    self.dict_to_csv[noms_stats] = statistique
                else:
                    noms_stats = get_noms.group()[1:]
                    self.dict_to_csv[noms_stats] = statistique
            except:
                pass
        return self.dict_to_csv

    def get_divers(self, pkm):
        if pkm in ["Morphéo", "Cheniselle", "Motisma", "Giratina", "Shaymin", "Arceus", "Boréas", "Meloetta", "Amphinobi", "Sapereau", "Pandespiègle", "Pandarbare"]:
            self.dict_to_csv['catégorie'] = "catégorie"
            self.dict_to_csv['taille'] = "taille"
            self.dict_to_csv['poids'] = "poids"
            self.dict_to_csv['couleur'] = "couleur"
            self.dict_to_csv['corps'] = "corps"
            self.dict_to_csv['Légendaire'] = 0
        else:
            # Catégorie
            categorie = self.driver.find_element(
                By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[9]/td')
            inner_cat = categorie.get_attribute('innerHTML')
            inner_cat = inner_cat.split('</a>')[-1]
            # print(inner_cat)
            self.dict_to_csv['catégorie'] = inner_cat

            # Taille
            taille_find = self.driver.find_element(
                By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[10]/td'
            )
            inner_taille = taille_find.get_attribute('innerHTML')
            inner_taille = inner_taille.split('>')
            inner_taille = inner_taille[0].replace(",", ".", 1)
            inner_taille = inner_taille.split(' m,')
            inner_taille = inner_taille[0]
            self.dict_to_csv['taille'] = inner_taille

            # Poids
            poids_find = self.driver.find_element(
                By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[11]/td'
            )
            inner_poids = poids_find.get_attribute('innerHTML')
            inner_poids = inner_poids.split('>')
            inner_poids = inner_poids[0].replace(",", ".", 1)
            inner_poids = inner_poids.split(' kg,')
            inner_poids = inner_poids[0]
            self.dict_to_csv['poids'] = inner_poids

            # Couleur
            color_find = self.driver.find_element(
                By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[19]/td'
            )
            inner_color = color_find.get_attribute('innerHTML')
            inner_color = inner_color.split('>&nbsp;')
            inner_color = inner_color[1]
            # print(inner_color)
            self.dict_to_csv['couleur'] = inner_color

            # Type de corps
            img_elem = self.driver.find_element(By.XPATH,
                                        "/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[22]/td/a/img")
            img_text = img_elem.get_attribute("alt")
            # print(img_text)
            self.dict_to_csv['corps'] = img_text

            self.dict_to_csv['Légendaire'] = 0
        return self.dict_to_csv

    def get_pkdex_nb(self):
        table_pkdex_nb = self.driver.find_element(
            By.XPATH, '/html/body/div[3]/div[3]/div[5]/div[1]/table[2]/tbody/tr[5]/td/table/tbody'
        )
        innerHTML = table_pkdex_nb.get_attribute("innerHTML")
        soup = BeautifulSoup(innerHTML, 'html.parser')
        # print(soup.prettify())
        row = soup.find_all('tr')

        # index
        i = 0
        list_pays = []
        list_no_pays = []
        for r in row:
            i += 1
            if i % 2 != 0:
                r_soup = r.find_all('strong')
                for stron in r_soup:
                    pays = stron.text
                    list_pays.append(pays)
            else:
                td_soup = r.find_all('td')
                for td in td_soup:
                    nopays = td.text
                    list_no_pays.append(nopays)
        j = 0
        for item in list_pays:
            self.dict_to_csv[item] = list_no_pays[j]
            j += 1

        return self.dict_to_csv
