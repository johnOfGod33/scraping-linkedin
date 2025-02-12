import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from . import utils
from .auth import authenticate

## charger les variables d'environnement pour la connexion
load_dotenv()

user_credentials = {
    "username": os.getenv("LINKEDIN_USERNAME"),
    "password": os.getenv("LINKEDIN_PASSWORD"),
}


DRIVER_PATH = os.getenv("DRIVER_PATH")
service = Service(executable_path=DRIVER_PATH)
driver = webdriver.Chrome(service=service)

authenticate(driver, user_credentials)
