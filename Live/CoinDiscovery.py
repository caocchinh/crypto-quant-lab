import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
import random

link = "https://coindiscovery.app/coin/dog"
className = "button.coin-voting.btn.btn-golden.bmux-vote.now"
chrome_options = ChromeOptions()

# chrome_options.add_argument("--headless")

firefox_options = FirefoxOptions()
# firefox_options.add_argument("--headless")
firefox_options.set_preference("dom.storage.enabled", False)

edge_options = webdriver.EdgeOptions()
edge_options.use_chromium = True
# edge_options.add_argument("headless")

rocket_count = 0




def windscribe(action, location=None):
    windscribe_cli_path = r"C:\\Program Files\\Windscribe\\windscribe-cli.exe"
    if location is None:
        command = f'"{windscribe_cli_path}" {action}'
    else:
        command = f'"{windscribe_cli_path}" {action} {location}'
    os.system(command)

def thread_function(name):
    while True:
        try:
            def main():
                global rocket_count
                windscribe("connect", random.sample(
                    ["crumpets", "Custard", "US", "Zurich", "Toronto", "Vancouver", "Paris", "Frankfurt", "Amsterdam",
                     "Fjord", "Bucharest", "Alphorn", "Lindenhof", "Istanbul", "Victoria"], 1)[0])
                time.sleep(11)
                if name == "firefox":
                    driver = webdriver.Firefox(options=firefox_options)
                elif name == "chrome":
                    driver = webdriver.Chrome(options=chrome_options)
                elif name == "edge":
                        driver = webdriver.Edge(options=edge_options)
                driver.maximize_window()
                driver.get(link)
                time.sleep(6)
                try:
                    button = driver.find_element("css selector", className)
                except Exception:
                    button = driver.find_element("css selector", className[:-4])

                driver.implicitly_wait(10)
                for i in range(1,15):
                    try:
                        button.click()
                        time.sleep(1)
                    except Exception:
                        rocket_count += 1
                        print(f"Votes smashed successfully: {rocket_count}")
                        break
                driver.quit()
                windscribe("disconnect")
            main()
            print("\n")
        except Exception:
            pass


thread_function("chrome")
