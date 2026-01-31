import time
from selenium.webdriver.common.by import By
from Metamask import MetaMask
import psutil
votes = 0


def main():
    global votes
    for i in range(1,1032):
        try:
            for proc in psutil.process_iter():
                try:
                    if 'chrome.exe' in proc.name().lower():
                        proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            mask = MetaMask("https://www.dexview.com/solana/Bt4bHXso7zYiNcXFrQVWPS7nemPqhwXiSjqRLPkZrA1U", isStealth=False, headless=False)
            driver = mask.driver
            driver.find_element("css selector", "button.chakra-button.css-73pxpg").click()
            time.sleep(1)
            driver.find_element(By.XPATH, "//*[contains(text(), 'Metamask')]").click()
            time.sleep(2)
            mask.return_to_metamask()
            time.sleep(3)
            driver.find_element(By.XPATH, '//button[@data-testid="page-container-footer-next"]').click()
            driver.find_element(By.XPATH, '//button[@data-testid="page-container-footer-next"]').click()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(3)
            driver.find_element("css selector", ".css-hn6sdl").click()
            time.sleep(3)
            mask.return_to_metamask()
            time.sleep(3)
            driver.find_element(By.XPATH, '//button[@data-testid="page-container-footer-next"]').click()
            time.sleep(1.3)
            driver.quit()
            votes += 1
            print(f"Vote smashed successfully: {votes}")
        except Exception:
            driver.quit()
            driver.quit()
            del driver
            del mask

if __name__ == "__main__":
    main()

