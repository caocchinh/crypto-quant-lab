from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Users\\Lenovo\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 5")
#options.add_argument(r"--user-data-dir=C:\Users\Admin\AppData\Local\Google\Chrome\User Data")
#options.add_argument('--profile-directory=Person 2')
#options.add_experimental_option("detach", True)
#options.add_argument("--disable-notifications")
#options.add_argument("--disable-infobars")


#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = webdriver.Chrome(options=options)


driver.maximize_window()
driver.get("https://app.pickupmusic.com/lesson-library")
time.sleep(1000000)
driver.maximize_window()
