import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
rocket_smashed = 0

link = "https://fomospider.com/coin/DOG"
className = "button.btn-1.btn-vote"
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
edge_options = webdriver.EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument("headless")


def spam(name):
    rocket_count = 0
    if name == "firefox":
        driver = webdriver.Firefox(options=firefox_options)
    elif name == "chrome":
        driver = webdriver.Chrome(options=chrome_options)
    elif name == "edge":
        driver = webdriver.Edge(options=edge_options)
    driver.get(link)
    while True:
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-1.btn-vote"))).click()
                time.sleep(5)
                rocket_count += 1
                print(f"Rockets smashed: {rocket_count}")
            except:
                pass
            time.sleep(65)

spam("firefox")