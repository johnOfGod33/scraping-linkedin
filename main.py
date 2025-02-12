import os
import random

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

from auth import authenticate
from scrape_job import scrape_jobs

load_dotenv()

user_credentials = {
    "username": os.getenv("LINKEDIN_USERNAME"),
    "password": os.getenv("LINKEDIN_PASSWORD"),
}

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    # Add more User-Agent strings as needed
]

random_user_agent = random.choice(user_agents)
# Récupération du chemin du driver Chrome à partir des variables d'environnement
DRIVER_PATH = os.getenv("DRIVER_PATH")

# Création d'un service Selenium avec le chemin du driver
service = Service(executable_path=DRIVER_PATH)

# Configuration des options pour le navigateur Chrome
options = Options()
options.add_argument(f"user-agent={random_user_agent}")

# Initialisation du driver Chrome avec le service défini
driver = webdriver.Chrome(service=service, options=options)

# Demande à l'utilisateur d'entrer un mot-clé pour la recherche d'emploi
keyword = input("Enter a keyword for the job search: ")

# Authentification sur LinkedIn avec le driver et les identifiants
authenticate(driver, user_credentials)

# Exécution du scraping des offres d'emploi en fonction du mot-clé fourni
scrape_jobs(driver, keyword=keyword)
