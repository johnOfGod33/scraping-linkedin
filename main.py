import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from auth import authenticate
from scrape_job import scrape_jobs

load_dotenv()

user_credentials = {
    "username": os.getenv("LINKEDIN_USERNAME"),
    "password": os.getenv("LINKEDIN_PASSWORD"),
}

# Récupération du chemin du driver Chrome à partir des variables d'environnement
DRIVER_PATH = os.getenv("DRIVER_PATH")

# Création d'un service Selenium avec le chemin du driver
service = Service(executable_path=DRIVER_PATH)

# Configuration des options pour le navigateur Chrome
Options = Options()

# Initialisation du driver Chrome avec le service défini
driver = webdriver.Chrome(service=service)

# Demande à l'utilisateur d'entrer un mot-clé pour la recherche d'emploi
keyword = input("Enter a keyword for the job search: ")

# Authentification sur LinkedIn avec le driver et les identifiants
authenticate(driver, user_credentials)

# Exécution du scraping des offres d'emploi en fonction du mot-clé fourni
scrape_jobs(driver, keyword=keyword)
