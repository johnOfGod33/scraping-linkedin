import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import load_cookies, save_cookies


def login(driver: webdriver.Chrome, user_credentials: dict):
    """
    Login to LinkedIn using provided user credentials.
    """
    print("start login function")

    links = driver.find_elements(By.TAG_NAME, "a")

    # get sign in link and click it
    for link in links:
        if link.text == "Sign in":
            link.click()
            break

    try:
        # wait for the login form to be present
        login_form = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login__form"))
        )

        # complete the login form
        username_input = login_form.find_element(By.ID, "username")
        password_input = login_form.find_element(By.ID, "password")

        username_input.send_keys(user_credentials["username"])
        password_input.send_keys(user_credentials["password"])

        login_form.submit()

        time.sleep(120)  # wait for handle captcha or bot detection if needed

        # save cookies after login
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
    Authenticate the user on LinkedIn.
    """
    driver.get("https://linkedin.com")

    driver = load_cookies(driver)

    driver.refresh()

    try:
        title = driver.title

        if "feed" in title.lower():
            print("Already logged in")

            time.sleep(10)
        else:
            print("Not logged in")
            time.sleep(30)
            # Si l'utilisateur n'est pas connecté, exécuter la fonction de connexion
            login(driver, user_credentials)
    except TimeoutException:
        print("Timeout while checking authentication")
        print("handle captcha or bot detection")
        time.sleep(60)
        cookies = driver.get_cookies()
        save_cookies(cookies)
        pass
