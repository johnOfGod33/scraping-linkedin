from selenium import webdriver

driver = webdriver.Chrome()  # start a session

url = "https://www.selenium.dev/documentation/webdriver/getting_started/first_script/"

driver.get(url)  # navigate to a web page

title = driver.title
cookies = driver.get_cookies()

print(f"Title: {title}")
print(f"Cookies: {cookies}")

# wating strategy
# the main challenge with selenium is to synchronize the the code with the current state of the browser.
# we want to make sure thata the element we want to interact with is present in the DOM and is visible before we try to interact with it.

# first methode
driver.implicitly_wait(10)  # for wating 10 seconds


driver.quit()  # end the session
