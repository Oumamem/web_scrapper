import requests
from bs4 import BeautifulSoup
import csv
import os


def scrape_navigation_bar(url):
    # Faites une requête HTTP pour obtenir le contenu HTML de la page
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erreur lors de la récupération de la page : {response.status_code}")
        return []

    # Analysez le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Trouvez la barre de navigation en utilisant les balises ou les classes CSS appropriées
    navigation_bar = soup.find("nav")
    navigation_menu = soup.find("li", class_="menu-item")

    # Extrayez tous les éléments de la barre de navigation
    if navigation_bar:
        navigation_elements = navigation_bar.find_all("a")
        navigation_items = [element.text for element in navigation_elements]
        return navigation_items
    if navigation_menu:
        navigation_elements = navigation_menu.find_all("a")
        navigation_items = [element.text for element in navigation_elements]
        return navigation_items


def append_navigation_to_csv(csv_file, navigation_items):
    # Append the navigation items to the CSV file or create it if it doesn't exist
    mode = "a" if os.path.exists(csv_file) else "w"
    with open(csv_file, mode, newline="") as file:
        writer = csv.writer(file)
        for item in navigation_items:
            writer.writerow([item])


if __name__ == "__main__":
    url_to_scrape = "https://www.ajtdetective.com/fr/detective-paris-2/"
    csv_file = "./navigations.csv"

    navigation_items = scrape_navigation_bar(url_to_scrape)

    if navigation_items:
        print("Éléments de la barre de navigation :")
        for item in navigation_items:
            print(item)

        # Add the navigation items to the CSV file or create it if it doesn't exist
        append_navigation_to_csv(csv_file, navigation_items)
        print("Éléments ajoutés au fichier CSV.")
    else:
        print("Aucun élément de la barre de navigation trouvé.")
