import json

from selenium import webdriver


def load_cookies(driver: webdriver.Chrome):
    try:
        with open("cookies.json", "r") as cookies_file:
            cookies = json.load(cookies_file)
            for cookie in cookies:
                driver.add_cookie(cookie)

        return driver
    except FileNotFoundError:
        return driver


def save_cookies(cookies: list):
    with open("cookies.json", "w") as cookies_file:
        json.dump(cookies, cookies_file)
        print("Cookies saved")
