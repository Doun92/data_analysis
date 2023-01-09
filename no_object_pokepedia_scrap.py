# Imports
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup

# Data
data_folder = Path("datasets/")

dataset_to_fill = f"{data_folder}/pokedex2.csv"

driver = webdriver.Firefox()

continue_scrp = True

pokemon = "Dialga"

url = f"https://www.pokepedia.fr/{pokemon}"

driver.get(url)

liste_pokemons = []

run=387

# TODO
# Dialga a deux poids et deux tailles: à faire comme pour le nav_exist et le table_types

# while run < 495:
while run < 388:
# Empty dictionnary
    pokedex_row = {}
    bodyContent = driver.find_element(By.ID, "mw-content-text")
    tableau_divers = bodyContent.find_elements(By.TAG_NAME, "table")[1]

    # Pour avoir le numéro national du pokemon et son nom en français
    thead = tableau_divers.find_element(By.TAG_NAME, "thead")
    pokedex_row["numéro"] = thead.find_element(
        By.TAG_NAME, "span").get_attribute('innerHTML')[-3:]
    pokedex_row["nom_fr"] = thead.find_elements(
        By.TAG_NAME, "th")[1].get_attribute('innerHTML')

    tbody = tableau_divers.find_element(By.TAG_NAME, "tbody")
    list_tr = tbody.find_elements(By.TAG_NAME, "tr")
    # TR00 = image

    # TR01 = nom japonais
    item01 = list_tr[1].find_element(By.TAG_NAME, "i")
    pokedex_row["nom_jp"] = item01.get_attribute('innerHTML')

    # TR02 = nom anglais
    item02 = list_tr[2].find_element(By.TAG_NAME, "td")
    pokedex_row["nom_en"] = item02.get_attribute('innerHTML')

    # TR03 = titre

    # TR04 = numéros de pokedex régionaux
    inside_table00 = list_tr[4].find_element(By.TAG_NAME, "tbody")
    list_trs = inside_table00.find_elements(By.TAG_NAME, "tr")
    # On index les lignes
    # Les lignes pairs sont les régions et les lignes impaires sont les nombres
    liste_regions = []
    liste_nombres = []
    for idx, tr in enumerate(list_trs):
        if idx % 2 == 0:
            tds = tr.find_elements(By.TAG_NAME, "td")
            for td in tds:
                # On doit jouer avec les régions qui ont des extensions
                strong_tag = td.find_element(By.TAG_NAME, "strong")
                if "sup" in strong_tag.get_attribute("innerHTML"):
                    a_tag = strong_tag.find_element(By.TAG_NAME, "a")
                    spans = strong_tag.find_elements(By.TAG_NAME, "span")
                    span_list = []
                    for span in spans: 
                        span_list.append(span.get_attribute("innerHTML"))
                    version = "".join(span_list)
                    region = a_tag.get_attribute("innerHTML") + "_" + version
                else:
                    # On doit ajouter ça au cas où le pokemon n'a pas encore de nombre affilié à cette région
                    try:
                        a_tag = strong_tag.find_element(By.TAG_NAME, "a")
                        region = a_tag.get_attribute("innerHTML")
                    except:
                        region = "Hisui"  
                liste_regions.append(region)
                # print(liste_regions)
        else:
            tds = tr.find_elements(By.TAG_NAME, "td")
            for td in tds:
                nombre_regional = td.get_attribute("innerHTML")
                if 'Hisui' in nombre_regional:
                    liste_nombres.append(0)
                else:
                    liste_nombres.append(nombre_regional)
                # print(liste_nombres)

    dict_pokedex_regionaux = {}
    for i, region in enumerate(liste_regions):
        dict_pokedex_regionaux[region] = liste_nombres[i]
    # On merge les deux dictionnaires
    pokedex_row = {**pokedex_row, **dict_pokedex_regionaux}
    # print(pokedex_row)

    # Types
    is_navigateur = list_tr[4+len(list_trs)+1].get_attribute("innerHTML")
    if "Navigateurs" or "numérotations" in str(is_navigateur):
        list_nb_nav = list_tr[4+len(list_trs)+1+1]
        inside_table_nav = list_nb_nav.find_element(By.TAG_NAME, "tbody")
        list_trs_nav = inside_table_nav.find_elements(By.TAG_NAME, "tr")
        nav_exist = True
    else:
        nav_exist = False
    # print(nav_exist)

    if nav_exist:
        types = list_tr[4+len(list_trs)+1+1+len(list_trs_nav)+1]
    else:
        types = list_tr[4+len(list_trs)+1]

    # On bouge dans l'image et on choppe le type
    liste_types = types.find_elements(By.TAG_NAME, "a")
    if len(liste_types) == 1:
        table_types = True
    else:
        table_types = False

    if table_types and nav_exist:
        types_nav_tab_h = list_tr[4+len(list_trs)+1+1+len(list_trs_nav)+2]
        liste_types_nav_tab_h = types_nav_tab_h.find_elements(By.TAG_NAME, "a")
        for idx, type in enumerate(liste_types_nav_tab_h):
            title = type.get_attribute("title")
            type = str(title).split()[0]
            pokedex_row[f"type {idx+1}"] = type
        types_nav_tab_b = list_tr[4+len(list_trs)+1+1+len(list_trs_nav)+3]
        liste_types_nav_tab_b = types_nav_tab_b.find_elements(By.TAG_NAME, "a")
        for idx, type in enumerate(liste_types_nav_tab_b):
            title = type.get_attribute("title")
            type = str(title).split()[0]
            pokedex_row[f"type {idx+1+2}"] = type
    elif table_types and nav_exist == False:
        types = list_tr[4+len(list_trs)+1]
    elif table_types == False and nav_exist:
        types = list_tr[4+len(list_trs)+1+1+len(list_trs_nav)+1]
        for idx, type in enumerate(liste_types[1:]):
            title = type.get_attribute("title")
            type = str(title).split()[0]
            pokedex_row[f"type {idx+1}"] = type
    else:
        types = list_tr[4+len(list_trs)+1]
        for idx, type in enumerate(liste_types[1:]):
            title = type.get_attribute("title")
            type = str(title).split()[0]
            pokedex_row[f"type {idx+1}"] = type




    # Catégorie
    if table_types and nav_exist:
        categorie = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                            4].find_element(By.TAG_NAME, "td")
    elif table_types and nav_exist == False:
        categorie = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                            3].find_element(By.TAG_NAME, "td")
    elif table_types == False and nav_exist:
        categorie = list_tr[4+len(list_trs)+1+1+len(list_trs_nav)+2].find_element(By.TAG_NAME, "td")
    else:
        categorie = list_tr[4+len(list_trs)+2].find_element(By.TAG_NAME, "td")
    cat_def = str(categorie.get_attribute("innerHTML")).split()[-1]
    pokedex_row["categorie"] = cat_def
    # print(pokedex_row)

    # Taille
    if "Tailles" in list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 3].get_attribute("innerHTML"):
        liste_tailles_exist = True
    else:
        liste_tailles_exist = False


    # On se dirige vers un système bien complqiué, l'ami
    if table_types and nav_exist and liste_tailles_exist:
        print("Â FAIRE AU BESOIN")
    elif table_types and nav_exist and liste_tailles_exist == False:
        taille = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                        5].find_element(By.TAG_NAME, "td")
        taille_def = str(taille.get_attribute("innerHTML")).split()[0]
        pokedex_row["taille_en_m"] = taille_def
    elif table_types and nav_exist == False and liste_tailles_exist:
        print("Â FAIRE AU BESOIN 2")
    elif table_types and nav_exist == False and liste_tailles_exist == False:
        taille = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                        4].find_element(By.TAG_NAME, "td")
        taille_def = str(taille.get_attribute("innerHTML")).split()[0]
        pokedex_row["taille_en_m"] = taille_def
    elif table_types == False and nav_exist and liste_tailles_exist:
        liste_tailles = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 4].find_elements(By.TAG_NAME, "td")
        for idx, taille in enumerate(liste_tailles):
            # print(taille.get_attribute("innerHTML"))
            taille_def = str(taille.get_attribute("innerHTML")).split()[0]
            pokedex_row[f"taille_en_m_{idx+1}"] = taille_def
    elif table_types == False and nav_exist and liste_tailles_exist == False:
        taille = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                            3].find_element(By.TAG_NAME, "td")
        taille_def = str(taille.get_attribute("innerHTML")).split()[0]
        pokedex_row["taille_en_m"] = taille_def
    elif table_types == False and nav_exist == False and liste_tailles_exist:
        print("Â FAIRE AU BESOIN 4")
    else:
        taille = list_tr[4+len(list_trs)+3].find_element(By.TAG_NAME, "td")
        taille_def = str(taille.get_attribute("innerHTML")).split()[0]
        pokedex_row["taille_en_m"] = taille_def

    # print(pokedex_row)

    # Poids
    # On se dirige vers un système bien complqiué, l'ami
    if table_types and nav_exist and liste_tailles_exist:
        if "Poids" in list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 6].get_attribute("innerHTML"):
            print("yes")
            liste_poids_exist = True
        else:
            print("no")
            liste_poids_exist = False
        print("Â FAIRE AU BESOIN 3")
    elif table_types and nav_exist and liste_tailles_exist == False:
        poids = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 6].find_element(By.TAG_NAME, "td")
        poids_def = str(poids.get_attribute("innerHTML")).split()[0]
        pokedex_row["poids_en_kg"] = poids_def
        
    elif table_types and nav_exist == False and liste_tailles_exist:
        print("Â FAIRE AU BESOIN 5")
        if "Poids" in list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 5].get_attribute("innerHTML"):
            print("yes")
            liste_poids_exist = True
        else:
            print("no")
            liste_poids_exist = False
    elif table_types and nav_exist == False and liste_tailles_exist == False:
        poids = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                         5].find_element(By.TAG_NAME, "td")
        poids = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 5].find_element(By.TAG_NAME, "td")
        poids_def = str(poids.get_attribute("innerHTML")).split()[0]
        pokedex_row["poids_en_kg"] = poids_def
    elif table_types == False and nav_exist and liste_tailles_exist:
        if "Poids" in list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 3
                              + len(liste_tailles)].get_attribute("innerHTML"):
            liste_poids = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 3 + len(liste_tailles)].find_elements(By.TAG_NAME, "td")
            for idx, poids in enumerate(liste_poids):
                print(poids)
                poids_def = str(poids.get_attribute("innerHTML")).split()[0]
                pokedex_row[f"poids_en_kg{idx+1}"]=poids_def
            liste_poids_exist = True
        else:
            print("no")
            liste_poids_exist = False
    elif table_types == False and nav_exist and liste_tailles_exist == False:
        poids = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +4].find_element(By.TAG_NAME, "td")
        poids_def = str(poids.get_attribute("innerHTML")).split()[0]
        pokedex_row["poids_en_kg"] = poids_def
    elif table_types == False and nav_exist == False and liste_tailles_exist:
        print("Â FAIRE AU BESOIN 7")
        if "Poids" in list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 4].get_attribute("innerHTML"):
            print("yes")
            liste_poids_exist = True
        else:
            print("no")
            liste_poids_exist = False
    else:
        print("Â FAIRE AU BESOIN 8")
        if "Poids" in list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 4].get_attribute("innerHTML"):
            print("yes")
            liste_poids_exist = True
        else:
            print("no")
            liste_poids_exist = False
        poids = list_tr[4+len(list_trs)+4].find_element(By.TAG_NAME, "td")
        poids_def = str(poids.get_attribute("innerHTML")).split()[0]
        pokedex_row["poids_en_kg"] = taille_def

    #Couleur
    if table_types and nav_exist:
        if liste_tailles_exist and liste_poids_exist:
            print("À changer 1")
        else:
            couleur = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                        14].find_element(By.TAG_NAME, "td")
            couleur_def = str(couleur.get_attribute(
                "innerHTML")).split(">")[-1]
            couleur_def = couleur_def.replace("&nbsp;", "")
            pokedex_row["couleur"] = couleur_def
    elif table_types and nav_exist == False:
        if liste_tailles_exist and liste_poids_exist:
            print("À changer 2")
        else:
            couleur = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                        13].find_element(By.TAG_NAME, "td")
            couleur_def = str(couleur.get_attribute(
                "innerHTML")).split(">")[-1]
            couleur_def = couleur_def.replace("&nbsp;", "")
            pokedex_row["couleur"] = couleur_def
    elif table_types == False and nav_exist:
        if liste_tailles_exist and liste_poids_exist:
            if "Couleurs" in list_tr[4+len(list_trs)+1+1+len(list_trs_nav) + 12+2].get_attribute("innerHTML"):
                liste_couleurs = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                                  12+2].find_elements(By.TAG_NAME, "img")                   
                for idx, couleur in enumerate(liste_couleurs):
                    print(couleur.get_attribute("innerHTML"))
                    couleur_def = str(couleur.get_attribute(
                        "title"))
                    pokedex_row[f"couleur_{idx}"] = couleur_def
                    liste_couleurs_exist = True
            else:
                couleur = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                                12+2].find_element(By.TAG_NAME, "td")
                couleur_def = str(couleur.get_attribute(
                    "innerHTML")).split(">")[-1]
                couleur_def = couleur_def.replace("&nbsp;", "")
                pokedex_row["couleur"] = couleur_def
                liste_couleurs_exist = False
        else:
            couleur = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                        12].find_element(By.TAG_NAME, "td")
            couleur_def = str(couleur.get_attribute(
                "innerHTML")).split(">")[-1]
            couleur_def = couleur_def.replace("&nbsp;", "")
            pokedex_row["couleur"] = couleur_def
    else:
        if liste_tailles_exist and liste_poids_exist:
            print("À changer 4")
        else:
            couleur = list_tr[4+len(list_trs) +
                              12].find_element(By.TAG_NAME, "td")
            couleur_def = str(couleur.get_attribute("innerHTML")).split(">")[-1]
            couleur_def = couleur_def.replace("&nbsp;", "")
            pokedex_row["couleur"] = couleur_def
    
    #Forme
    # TODO: Voir ce qui se passe ici
    # TODO: ça devient ingérable, régler le souci avec des fonctions
    print(f"mon print, {pokedex_row}")
    print(f"{liste_tailles_exist} and {liste_poids_exist} and {liste_couleurs_exist}")
    if table_types and nav_exist:
        forme_img = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                            17].find_element(By.TAG_NAME, "td")
    elif table_types and nav_exist == False:
        print("là")
        if liste_tailles_exist and liste_poids_exist and liste_couleurs_exist:
            print("ici")
        else:    
            forme_img = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                                16].find_element(By.TAG_NAME, "td")
    elif nav_exist:
        forme_img = list_tr[4+len(list_trs)+1+1+len(list_trs_nav) +
                        15].find_element(By.TAG_NAME, "td")
    else:
        forme_img = list_tr[4+len(list_trs)+15].find_element(By.TAG_NAME, "td")

    formes = forme_img.find_elements(By.TAG_NAME, "a")
    if len(formes) == 1:

        pokedex_row["forme"] = formes[0].get_attribute('title')
    else:
        pokedex_row["forme"] = formes[1].get_attribute('title')

    # Statistiques
    find_stats = bodyContent.find_elements(By.TAG_NAME, "tbody")
    for th in find_stats:
        if "Statistiques indicatives" in str(th.get_attribute('innerHTML')):
            list_tr = th.find_elements(By.TAG_NAME,"tr")
            # 03: PV
            td = list_tr[3].find_elements(By.TAG_NAME, "td")
            nb_pv = str(td[1].get_attribute("innerHTML").replace("\n", ""))
            pokedex_row["points_de_vie"]=nb_pv
            # 04: ATK
            td = list_tr[4].find_elements(By.TAG_NAME, "td")
            nb_atk = str(td[1].get_attribute("innerHTML").replace("\n", ""))
            pokedex_row["attaque"] = nb_atk
            # # 05: DEF
            # print(list_tr[5].get_attribute("innerHTML"))
            td = list_tr[5].find_elements(By.TAG_NAME, "td")
            nb_def = str(td[1].get_attribute("innerHTML").replace("\n", ""))
            pokedex_row["defense"] = nb_def
            # # 06: ASP
            # print(list_tr[6].get_attribute("innerHTML"))
            td = list_tr[6].find_elements(By.TAG_NAME, "td")
            nb_atk_spe = str(td[1].get_attribute("innerHTML").replace("\n", ""))
            pokedex_row["attaque_speciale"] = nb_atk_spe
            # # 07: DSP
            # print(list_tr[7].get_attribute("innerHTML"))
            td = list_tr[7].find_elements(By.TAG_NAME, "td")
            nb_atk_spe = str(td[1].get_attribute("innerHTML").replace("\n", ""))
            pokedex_row["defense_speciale"] = nb_atk_spe
            # # 08: VIT
            # print(list_tr[8].get_attribute("innerHTML"))
            td = list_tr[8].find_elements(By.TAG_NAME, "td")
            vitesse = str(td[1].get_attribute("innerHTML").replace("\n", ""))
            pokedex_row["vitesse"] = vitesse

    # Bouton suivant
    bouton_suivant = bodyContent.find_element(
        By.XPATH, "/html/body/div[3]/div[3]/div[5]/div[1]/table[1]/tbody/tr[1]/td[9]/a")
    bouton_suivant.click()

    liste_pokemons.append(pokedex_row)

    run += 1

# df = pd.DataFrame([[liste_pokemons]])
df = pd.json_normalize(liste_pokemons)
print(df)
df.to_csv('poketest.csv', index=False)