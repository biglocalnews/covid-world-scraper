import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def scrape():
    url = 'https://covid.saude.gov.br/'
    opts = Options()
    opts.headless = True
    data = []
    try:
        driver = webdriver.Firefox(
            firefox_profile=ff_profile(),
            options=opts
        )
        driver.get(url)
        buttons = driver.find_elements_by_tag_name('ion-button')
        for button in buttons:
            if button.text.lower().strip() == 'arquivo csv':
                button.click()
                # NOTE: Timer needed to give download
                # time to complete
                time.sleep(10)
                break
    finally:
        driver.quit()


def ff_profile(download_dir=os.getcwd()):
    # Configure Firefox profile to avoid triggering pop-up
    # that requests permission to download, per Selenium docs:
    # https://selenium-python.readthedocs.io/faq.html#how-to-auto-save-files-using-custom-firefox-profile
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", download_dir)
    fp.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    return fp



if __name__ == '__main__':
    scrape()
