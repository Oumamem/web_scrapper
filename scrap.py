# Importer les modules
import requests
import csv
from bs4 import BeautifulSoup

# Adresse du site Internet
url = "https://investipole.fr/"
# Exécuter la requête GET
response = requests.get(url)
# Parser le document HTML BeautifulSoup obtenu à partir du code source
html = BeautifulSoup(response.text, "html.parser")
# Extraire toutes les citations et tous les auteurs du document HTML
quotes_html = html.find_all("span", class_="item_text")
# Rassembler les citations dans une liste
quotes = list()
for quote in quotes_html:
    quotes.append(quote.text)
for t in zip(quotes):
    print(t)
# Enregistrer les citations et les auteurs dans un fichier CSV dans le répertoire actuel
# Ouvrez le fichier avec Excel / LibreOffice, etc.
with open("./zitate.csv", "w") as csv_file:
    csv_writer = csv.writer(csv_file, dialect="excel")
    csv_writer.writerows(zip(quotes))
