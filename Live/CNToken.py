import random
import threading
import time

import psutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


link = "https://cntoken.io/coin/41975"
className = "button.el-button.vote-btn.el-button--success.is-plain"
error_class = ".el-message.el-message--error"
success_class = ".el-message.el-message--success"
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
edge_options = webdriver.EdgeOptions()
edge_options.use_chromium = True
edge_options.add_argument("headless")
rocket_count = 0
failed_count = 0
rocket_temp = 0

locations = [
    'Piedmont', 'Dallas', 'Ammo', 'BBQ', 'Ranch', 'Trinity', 'Denver', 'Barley',
    'Kansas City', 'Glinda', 'Boston', 'Harvard', 'MIT', 'Buffalo', 'Bill', 'Charlotte', 'Earnhardt',
    'Chicago', 'Cub', 'The L', 'Wrigley', 'Cleveland', 'Brown', 'Detroit', 'Coney Dog', 'Miami',
    'Florida Man', 'Snow', 'Vice', 'New Jersey', 'Situation', 'New York', 'Empire', 'Grand Central',
    'Insomnia', 'Orlando', 'Tofu Driver', 'Philadelphia', 'Fresh Prince', 'Sunny', 'South Bend',
    'Hawkins', 'Tampa', 'Cuban Sandwich', 'Washington DC', 'Precedent', 'Bend', 'Oregon Trail',
    'Las Vegas', 'Casino', 'Los Angeles', 'Cube', 'Dogg', 'Eazy', 'Lamar', 'Pac', 'Phoenix', 'Floatie',
    'San Francisco', 'Sanitation', 'San Jose', 'Santana', 'Santa Clara', 'Seattle', 'Cobain', 'Cornell',
    'Hendrix', 'Radiohall', 'Halifax', 'Crosby', 'Montreal', 'Bagel Poutine', 'Expo 67', 'Toronto',
    'Comfort Zone', 'The 6', 'Vancouver', 'Granville', 'Stanley', 'Vansterdam', 'Mansbridge', 'Vienna',
    'Boltzmann', 'Hofburg', 'Brussels', 'Guildhouse', 'Sofia', 'Nevski', 'Zagreb', 'Tkalciceva', 'Nicosia',
    'Blue Lagoon', 'Prague', 'Staromak', 'Vltava', 'LEGO', 'Tallinn', 'Lennujaam', 'Helsinki', 'Tram',
    'Marseille', 'La Marseillaise', 'Jardin', 'Seine', 'Frankfurt', 'Castle', 'Wurstchen', 'Athens',
    'Agora', 'Odeon', 'Budapest', 'Danube', 'Reykjavik', 'Fuzzy Pony', 'Reyka', 'Dublin', 'Dullahan',
    'Grafton', 'Guinness', 'Ashdod', 'Yam Park', 'Milan', 'Duomo', 'Galleria', 'Rome', 'Colosseum',
    'Riga', 'Daugava', 'Saeima', 'Vilnius', 'Neris', 'Luxembourg', 'Chemin', 'Chisinau', 'Dendrarium',
    'Amsterdam', 'Bicycle', 'Canal', 'Red Light', 'Tulip', 'Skopje', 'Vardar', 'Oslo', 'Fjord', 'Gdansk',
    'Motlawa', 'Curie', 'Vistula', 'Lisbon', 'Bairro', 'Bucharest', 'No Vampires', 'Bratislava', 'Devin Castle',
    'Barcelona', 'Batllo', 'Madrid', 'Prado', 'Stockholm', 'Djurgarden', 'Ikea', 'Syndrome', 'Zurich', 'Alphorn',
    'Altstadt', 'Lindenhof', 'Edinburgh', 'Keeper Willie', 'London', 'Biscuits', 'Crumpets', 'Custard', 'Manchester',
    'United', 'The Tube', 'Tirana', 'Besa', 'Novi Travnik', 'Pisanica', 'Sarajevo', 'Burek', 'Tbilisi', 'Ghvino',
    'Accra', 'Best Jollof', 'Mumbai', 'Mahim', 'Nairobi', 'Sigiria', 'Moscow', 'Goodbye Lenin', 'Saint Petersburg',
    'Hermitage', 'Shnur', 'Belgrade', 'Rakia', 'Johannesburg', 'District', 'Lindfield', 'Springbok', 'Istanbul',
    'Galata', 'Lygos', 'Kyiv', 'Ghost', 'Adelaide', 'Lofty', 'Oval', 'Brisbane', 'Bad Koala', 'Good Koala',
    'Melbourne', 'Port Phillip', 'Yarra', 'Perth', 'Herdsman', 'Sydney', 'Opera House', 'Squidney', 'Auckland',
    'Hauraki', 'Parnell', 'Phnom Penh', 'Botum Pagoda', 'Hong Kong', 'Phooey', 'Victoria', 'Jakarta', 'Ancol',
    'Old Town', 'Shinkansen', 'Wabi-sabi', 'Kuala Lumpur', 'Perdana', 'Manila', 'Pasig', 'Garden', 'Marina Bay',
    'SMRT', 'Han River', 'Hangang', 'Taipei', 'Datong', 'Hangover', 'Lumphini', 'Dubai', 'Khalifa', 'Hanoi',
    'Red River', 'Kaiju', 'Buenos Aires', 'Tango', 'Sao Paulo', 'Mercadao', 'Pinacoteca', 'Santiago', 'Cueca',
    'Bogota', 'Rololandia', 'Quito', 'Cuy', 'Guadalajara', 'Crudo', 'Mexico City', 'Cojones', 'Panama City',
    'Papers', 'Lima', 'Amaru', 'Troll', 'Station'
]

def windscribe(action, location):
    command = f'"C:\\Program Files\\Windscribe\\windscribe-cli.exe" {action} "{location}"'
    os.popen(command)

def kill():
    try:
        for proc in psutil.process_iter():
            try:
                if 'firefox.exe' in proc.name().lower():
                    proc.kill()
            except (
                    psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception:
        pass
    try:
        for proc in psutil.process_iter():
            try:
                if 'chrome.exe' in proc.name().lower():
                    proc.kill()
            except (
                    psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception:
        pass
    try:
        for proc in psutil.process_iter():
            try:
                if 'msedge.exe' in proc.name().lower():
                    proc.kill()
            except (
                    psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception:
        pass
def thread_function(name):
    while True:
        def main():
            attempt = 0
            try:
                if name == "firefox":
                    driver = webdriver.Firefox(options=firefox_options)
                elif name == "chrome":
                    driver = webdriver.Chrome(options=chrome_options)
                elif name == "edge":
                    driver = webdriver.Edge(options=edge_options)
                driver.get(link)
                WebDriverWait(driver, 9).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "button.el-button.vote-btn.el-button--success.is-plain"))).click()
                WebDriverWait(driver, 9).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".el-message")))

                def check():
                    global attempt
                    global rocket_count
                    global failed_count
                    global rocket_temp
                    try:
                        if driver.find_element("css selector", error_class):
                            failed_count += 1
                            print(f"Rockets smashed successfully: {rocket_count}")
                            print(f"Rockets smashed unsuccessfully: {failed_count}")
                            attempt = 0
                            raise AssertionError(f"")
                    except AssertionError:
                        raise AssertionError(f"")
                    except Exception:
                        try:
                            if driver.find_element("css selector", success_class):
                                driver.quit()
                                rocket_count += 1
                                rocket_temp += 1
                                print(f"Rockets smashed successfully: {rocket_count}")
                                attempt = 0
                                # if rocket_temp > 0:
                                #     time.sleep(random.randint(2,7))
                                #     if rocket_temp > 100:
                                #         kill()
                                #         windscribe("connect", random.choice(locations))
                                #         time.sleep(12)
                                #         rocket_temp = 0

                        except Exception:
                            if attempt < 40:
                                time.sleep(0.1)
                                attempt += 1
                                check()
                            else:
                                attempt = 0
                                driver.quit()

                check()
            except AssertionError:
                driver.quit()
                time.sleep(15)
            except Exception:
                main()

        main()


threads = []
kill()
for i in ["edge", "firefox", "chrome"]:
    thread = threading.Thread(target=thread_function, args=(i,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

