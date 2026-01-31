class MetaMask:
    def __init__(self, url, isStealth, headless):
        import time
        from selenium.webdriver import Chrome
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.common.by import By
        import undetected_chromedriver as uc
        link = "chrome-extension://nifkofpldbfokpagefljinciaamghfii/home.html#onboarding/welcome"
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless")
        if isStealth:
            chrome_options.add_argument(r'--load-extension=C:\Users\lenovo\AppData\Local\Temp\scoped_dir83196_1457718906\extension_nifkofpldbfokpagefljinciaamghfii')
            driver = uc.Chrome(options=chrome_options)
            time.sleep(10000)
        else:
            chrome_options.add_extension(
                r'C:\Users\lenovo\OneDrive\Bitcoin\Live\MetaMask.crx')
            driver = Chrome(options=chrome_options)
            time.sleep(10000)

        driver.get(link)
        driver.maximize_window()
        driver.switch_to.window(driver.window_handles[1])
        driver.get(url)
        driver.switch_to.window(driver.window_handles[0])
        try:
            driver.find_element("css selector", "input#onboarding__terms-checkbox").click()
            driver.find_element("css selector", "button.button.btn--rounded.btn-primary").click()
            driver.find_element("css selector", "button.button.btn--rounded.btn-primary.btn--large").click()
            driver.find_element("css selector", "input.check-box.far.fa-square").click()
            driver.find_element(By.XPATH, '//input[@data-testid="create-password-new"]').send_keys("12345678")
            driver.find_element(By.XPATH, '//input[@data-testid="create-password-confirm"]').send_keys("12345678")
            driver.find_element("css selector",
                                "button.button.btn--rounded.btn-primary.btn--large.create-password__form--submit-button").click()
            time.sleep(1)
            driver.find_element("css selector",
                                "button.mm-box.mm-text.mm-button-base.mm-button-base--size-lg.mm-button-base--block.mm-button-secondary.mm-text--body-md-medium.mm-box--padding-0.mm-box--padding-right-4.mm-box--padding-left-4.mm-box--display-inline-flex.mm-box--justify-content-center.mm-box--align-items-center.mm-box--color-primary-default.mm-box--background-color-transparent.mm-box--rounded-pill.mm-box--border-color-primary-default.box--border-style-solid.box--border-width-1").click()
            driver.find_element("css selector", "input.check-box.skip-srp-backup-popover__checkbox.far.fa-square").click()
            driver.find_element(By.XPATH, '//button[@data-testid="skip-srp-backup"]').click()
            driver.find_element("css selector", "button.button.btn--rounded.btn-primary").click()
            driver.find_element("css selector", "button.button.btn--rounded.btn-primary").click()
            driver.find_element("css selector", "button.button.btn--rounded.btn-primary").click()
            driver.switch_to.window(driver.window_handles[1])
        except Exception as e:
            print(e)
            driver.quit()
        self.driver = driver

    def return_to_metamask(self):
        all_handles = self.driver.window_handles
        extension_title = "MetaMask"
        count = 0
        for handle in all_handles:
            self.driver.switch_to.window(handle)
            if self.driver.title == extension_title:
                count += 1
                if count == 2:
                    break