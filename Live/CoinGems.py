
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os

locations = [
    'Mountain', 'Piedmont', 'Dallas', 'Ammo', 'BBQ', 'Ranch', 'Trinity', 'Denver', 'Barley',
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


def CoinsGem():
    driver = webdriver.Chrome()
    try:
        className = ".votes_btnVote__qci38"
        driver.maximize_window()
        driver.get('https://coinsgem.com/token/vEerjGVUQy1AuGXtyrgj5szKrGD3rTuyo2QqhdcHZSS')
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, className)))
        driver.execute_script("document.body.style.transform = 'scale(0.30)';")
        driver.execute_script("document.body.style.transformOrigin = 'top left';")
        button = driver.find_element(By.CSS_SELECTOR,className)
        driver.execute_script("arguments[0].click();", button)
        if WebDriverWait(driver, 20-5).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, className),
                                             "You can vote again in 8 hours")):
            driver.quit()
            return 1
        else:
            driver.quit()
            return 0
    except Exception:
        driver.quit()
        return 0


def windscribe(action, location):
    command = f'"C:\\Program Files\\Windscribe\\windscribe-cli.exe" {action} "{location}"'
    os.popen(command)


def main():
    rocket = 0
    bruh = 0
    for location in locations:
        windscribe("connect", location)
        try:
            result = CoinsGem()
            if result:
                rocket += 1
                print(f"Rockets smashed sucessfully: {rocket}")
            else:
                bruh += 1
                print(f"Failed attempts: {bruh}")
        except Exception:
            bruh += 1
            print(f"Failed attempts: {bruh}")


if __name__ == "__main__":
    while True:
        main()