from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from . import utils


def login(driver: webdriver.Chrome, user_credentials: dict):
    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        if link.text == "Sign in":
            link.click()
            break

    try:
        login_form = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "login__form"))
        )

        username_input = login_form.find_element(By.ID, "username")
        password_input = login_form.find_element(By.ID, "password")
        username_input.send_keys(user_credentials["username"])
        password_input.send_keys(user_credentials["password"])

        login_form.submit()

        WebDriverWait(driver, 10).until(EC.url_contains("linkedin.com/feed"))

        cookies = driver.get_cookies()

        utils.save_cookies(cookies)
    except NoSuchElementException:
        print("Login form not found")
    except TimeoutException:
        print("Login form not found")
    finally:
        driver.quit()


def authenticate(driver: webdriver.Chrome):
    driver.get("https://linkedin.com")

    driver = utils.load_cookies(driver)

    driver.refresh()

    try:
        current_url = driver.current_url
        if "linkedin.com/feed" in current_url:
            print("Already logged in")
            driver.quit()
        else:
            login(driver)
    except TimeoutException:
        print("Timeout")
        driver.quit()
