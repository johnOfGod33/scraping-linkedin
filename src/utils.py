import csv
import json
import os
import re
import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

from ai.ai_service import AIService
from models.job_offers import JobOffers

load_dotenv()


def load_cookies(driver: webdriver.Chrome):
    """load cookies from a JSON file and add them to the Selenium WebDriver."""
    try:
        with open("cookies.json", "r") as cookies_file:
            cookies = json.load(cookies_file)
            for cookie in cookies:
                driver.add_cookie(cookie)

        return driver
    except FileNotFoundError:
        print("No cookies found")
        return driver


def save_cookies(cookies: list):
    """Sauvegarde les cookies dans un fichier JSON."""
    with open("cookies.json", "w") as cookies_file:
        json.dump(cookies, cookies_file)
        print("Cookies saved")  # Confirmation de la sauvegarde


def save_to_csv(data: list, filename: str):
    """Sauvegarde les données d'une offre d'emploi dans un fichier CSV."""

    # Vérifier si le fichier existe déjà
    file_exists = False
    try:
        with open(filename, "r"):
            file_exists = True
    except FileNotFoundError:
        pass

    # Ouvrir le fichier en mode ajout
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Si le fichier n'existe pas, ajouter l'en-tête
        if not file_exists:
            writer.writerow(
                ["Title", "Company", "Date Posted", "Applicants", "Offer Types", "URL"]
            )

        # Ajouter les données dans le fichier CSV
        writer.writerow(data)


async def get_job_details(driver: webdriver.Chrome, job_url: str) -> JobOffers:
    """Get the job details from a job URL using Selenium and AIService to extract job offers."""

    driver.get(job_url)
    page_text = driver.find_element("tag name", "body").text
    job_offer = await AIService().extract_job_offers(page_text)

    time.sleep(10)
    return job_offer


def search_jobs(driver: webdriver.Chrome, keyword: str):
    """Effectue une recherche d'offres d'emploi sur LinkedIn et retourne la liste des URLs des offres trouvées."""

    # Construire l'URL de recherche avec le mot-clé
    search_url = (
        f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}"
    )
    base_url = "https://www.linkedin.com"
    driver.get(search_url)  # Charger la page des résultats de recherche

    html = driver.page_source  # Récupérer le HTML de la page
    soup = BeautifulSoup(html, "html.parser")  # Parser le HTML avec BeautifulSoup

    # Trouver le conteneur des offres d'emploi
    job_container = soup.find("div", {"class": "scaffold-layout__list"})

    if not job_container:
        print("No jobs found.")  # Afficher un message si aucune offre n'est trouvée
        return []

    # Extraire les offres d'emploi
    jobs = job_container.find_all("li")
    job_links = []

    for job in jobs:
        link = job.find("a")
        if link:
            job_links.append(f'{base_url}{link["href"]}')

    return job_links


""" def scroll_to_bottom(driver):
    # Scroll to the bottom of the page
    old_position = driver.execute_script("return window.pageYOffset;")
    while True:
        # Execute JavaScript to scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait for the page to load
        time.sleep(
            3
        )  # This delay will depend on the connection speed and server response time
        new_position = driver.execute_script("return window.pageYOffset;")
        if new_position == old_position:
            break  # Exit the loop if the page hasn't scrolled, meaning end of page
        old_position
 """


def driver_setup() -> webdriver.Chrome:
    options = get_default_chrome_option()
    # options.timeouts = {"implicit": 5000, "pageLoad": 10000}

    # Use ChromeDriverManager to automatically download the latest compatible version
    service = Service(ChromeDriverManager().install())
    # options.proxy = Proxy({"proxyType": ProxyType.DIRECT})

    driver = webdriver.Chrome(options=options, service=service)
    print("driver setup")
    return driver


def get_default_chrome_option() -> Options:
    ua = UserAgent()
    user_agent = ua.random
    print(f"Using User-Agent: {user_agent}")
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-images")
    options.add_argument("--disable-javascript")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(f"--user-agent={user_agent}")

    return options
