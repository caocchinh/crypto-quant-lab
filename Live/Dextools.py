import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Metamask import MetaMask
import psutil
from selenium.webdriver.common.by import By
import win32api, win32con
from selenium.webdriver.common.keys import Keys


def cloudfare_click(x,y, move=True):
    if move:
        win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

from seleniumbase import SB

def verify_success(sb):
    sb.assert_element('img[alt="Logo Assembly"]', timeout=8)
    sb.sleep(4)


def main():
    coin_page = "https://www.dextools.io/app/en/solana/pair-explorer/JD5GxSgcmHAsyir6CZP81pM1zsHZRki1pp3UYPqWshua?t=1711466232875"
    try:
        for proc in psutil.process_iter():
            try:
                if 'chrome.exe' in proc.name().lower():
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        mask = MetaMask("https://www.dextools.io/app/en/user/account", isStealth=True,
                        headless=False)
        driver = mask.driver
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.card__close"))).click()
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.btn.btn-info.ng-star-inserted"))).click()
        time.sleep(3)
        shadow_host = driver.find_element(By.CSS_SELECTOR, "w3m-modal")
        shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
        inner_shadow_host = shadow_root.find_element("css selector", 'w3m-router')
        inner_shadow_root = driver.execute_script("return arguments[0].shadowRoot", inner_shadow_host)
        inner_inner_shadow_host = inner_shadow_root.find_element("css selector", "w3m-connect-view")
        inner_inner_shadow_root = driver.execute_script("return arguments[0].shadowRoot", inner_inner_shadow_host)
        inner_inner_shadow_root.find_element("css selector", 'wui-list-wallet[name="MetaMask"]').click()
        time.sleep(2)
        mask.return_to_metamask()
        time.sleep(3.5)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="page-container-footer-next"]'))).click()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="page-container-footer-next"]'))).click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//button[@data-process-id="connectWallet"]').click()
        time.sleep(4)
        mask.return_to_metamask()
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//button[@data-testid="page-container-footer-next"]'))).click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[1])
        driver.get(coin_page)
        time.sleep(7)
        driver.find_element(By.TAG_NAME, 'html').send_keys(Keys.END)
        time.sleep(0.5)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.d-block.mb-1.action.buy-color.ng-star-inserted'))).click()
        time.sleep(6)


        cloudfare_click(120, 405)
        time.sleep(4)
        driver.find_element("css selector", 'app-new-pair-1221result-item.ng-tns-c1718992358-10.ng-tns-c199158450-9.ng-star-inserted').click()
    except Exception as e:
        print(e)
        time.sleep(100000)


# for i in range(1, 10000):
#     try:
#         main()
#         time.sleep(999991919191)
#     except Exception:
#         continue

# main()
#
with SB(uc_cdp=True, undetected=True, uc_cdp_events=True, uc_subprocess=True,guest_mode=True, extension_dir=r"C:\Users\lenovo\AppData\Local\Temp\scoped_dir19992_323363100\extension_nkbihfbeogaeaoehlefnkodbefgpgknn") as driver:
    driver.open("https://www.dextools.io/app/en/solana/pair-explorer/JD5GxSgcmHAsyir6CZP81pM1zsHZRki1pp3UYPqWshua?t=1711466232875")
    try:
        verify_success(driver)
    except Exception:
        if driver.is_element_visible('input[value*="Verify"]'):
            driver.click('input[value*="Verify"]')
        elif driver.is_element_visible('iframe[title*="challenge"]'):
            driver.switch_to_frame('iframe[title*="challenge"]')
            driver.click("span.mark")
        else:
            time.sleep(10000)
            driver.click()
        try:
            verify_success(driver)
        except Exception:
            time.sleep(10000)
            driver.click()
