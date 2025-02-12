import csv
import json
import re
import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from selenium import webdriver


def load_cookies(driver: webdriver.Chrome):
    """Charge les cookies à partir d'un fichier JSON et les applique au navigateur."""
    try:
        with open("cookies.json", "r") as cookies_file:
            cookies = json.load(cookies_file)
            for cookie in cookies:
                driver.add_cookie(cookie)

        return driver
    except FileNotFoundError:
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


def get_job_details(driver, job_url):
    """Récupère les détails d'une offre d'emploi à partir de son URL."""

    driver.get(job_url)
    page_html = driver.page_source
    soup_page = BeautifulSoup(page_html, "html.parser")

    # Extraire le titre du job
    title = soup_page.find("h1", class_="t-24 t-bold inline").text.strip()

    # Extraire le nom de l'entreprise
    company_name = soup_page.find(
        "div", class_="job-details-jobs-unified-top-card__company-name"
    ).text.strip()

    # Extraire les détails supplémentaires sur l'offre
    job_details = soup_page.find("div", class_="t-black--light mt2").text.strip()
    details = job_details.split(" · ")  # Séparer les détails par " · "

    # Vérifier si la date est relative (ex: "3 days ago") ou un autre format (ex: "Reposted")
    relative_date = details[1]
    match = re.search(r"(\d+)", relative_date)  # Recherche d'un nombre dans la chaîne

    if match:
        days_ago = int(match.group(1))  # Extraire le nombre de jours
        posted_date = datetime.now() - timedelta(
            days=days_ago
        )  # Calculer la date exacte
    else:
        posted_date = datetime.now()  # Si "Reposted", utiliser la date actuelle

    # Extraire le nombre de candidats ayant postulé
    applicants = details[2] if len(details) > 2 else "N/A"

    # Extraire les types d'offre (CDI, CDD, Stage, etc.)
    offer_types = []
    offer_elements = soup_page.find_all("span", class_="ui-label text-body-small")
    for offer in offer_elements:
        offer_types.append(offer.text.strip())

    job_data = [
        title,
        company_name,
        posted_date.strftime("%Y-%m-%d %H:%M:%S"),  # Formatage de la date
        applicants,
        ", ".join(offer_types),
        job_url,
    ]

    time.sleep(10)
    return job_data


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
