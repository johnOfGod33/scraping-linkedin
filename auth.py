from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import load_cookies, save_cookies


def login(driver: webdriver.Chrome, user_credentials: dict):
    """
    Se connecte à LinkedIn en utilisant les informations d'identification de l'utilisateur.
    """

    # Recherche tous les liens présents sur la page
    links = driver.find_elements(By.TAG_NAME, "a")

    # Trouver et cliquer sur le lien "Sign in"
    for link in links:
        if link.text == "Sign in":
            link.click()
            break

    try:
        # Attendre que le formulaire de connexion apparaisse
        login_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login__form"))
        )

        # Récupérer les champs d'identifiant et de mot de passe
        username_input = login_form.find_element(By.ID, "username")
        password_input = login_form.find_element(By.ID, "password")

        # Entrer les identifiants de connexion
        username_input.send_keys(user_credentials["username"])
        password_input.send_keys(user_credentials["password"])

        # Soumettre le formulaire
        login_form.submit()

        # Attendre que l'URL change et contienne "linkedin.com/feed", indiquant une connexion réussie
        WebDriverWait(driver, 10).until(EC.url_contains("linkedin.com/feed"))

        # Récupérer et sauvegarder les cookies après la connexion
        cookies = driver.get_cookies()
        save_cookies(cookies)

    except NoSuchElementException:
        print("Login form not found")
    except TimeoutException:
        print("Login process timed out")
    finally:
        pass


def authenticate(driver: webdriver.Chrome, user_credentials: dict):
    """
    Authentifie l'utilisateur sur LinkedIn en utilisant les cookies si disponibles,
    sinon procède à une connexion manuelle.
    """

    # Accéder à la page d'accueil de LinkedIn
    driver.get("https://linkedin.com")

    # Charger les cookies sauvegardés pour éviter une reconnexion manuelle
    driver = load_cookies(driver)

    # Rafraîchir la page après avoir chargé les cookies
    driver.refresh()

    try:
        # Vérifier si l'utilisateur est déjà connecté
        current_url = driver.current_url
        if "linkedin.com/feed" in current_url:
            print("Already logged in")
        else:
            # Si l'utilisateur n'est pas connecté, exécuter la fonction de connexion
            login(driver, user_credentials)
    except TimeoutException:
        print("Timeout while checking authentication")
