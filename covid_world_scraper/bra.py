import csv
import logging
import os
import openpyxl
from pathlib import Path

from retrying import retry
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .country_scraper import CountryScraper

import pandas as pd

logger = logging.getLogger(__name__)

class Bra(CountryScraper):

    def pre_process(self):
        # Remove any old non-standard and/or partial files
        previous = self.raw_dir.glob("HIST*")
        for p in previous:
            p.unlink()

    def fetch(self):
        url = 'https://covid.saude.gov.br/'
        opts = Options()
        opts.headless = True
        data = []
        driver = webdriver.Firefox(
            firefox_profile=self.ff_profile(str(self.raw_dir)),
            options=opts
        )
        try:
            driver.get(url)
            buttons = driver.find_elements_by_tag_name('ion-button')
            for button in buttons:
                if button.text.lower().strip() == 'arquivo csv':
                    button.click()
                    target_file = self._get_file_name(self.raw_dir)
                    logger.info('Downloaded {}'.format(target_file))
                    standardized_name = self._rename_xlxs(target_file)
                    logger.info('Renamed file to {}'.format(standardized_name))
                    return standardized_name
        finally:
            driver.quit()

    def extract(self, raw_data_path):

        # start to pandas solution
        # df = pd.read_excel(raw_data_path, sheet_name=None)
        # df['Sheet 1'].to_csv('output.csv')

        #start to openpyxl solution 
        wb = openpyxl.load_workbook(raw_data_path)[0]
        # sh = wb.get_active_sheet()
        with open('test.csv', 'wb') as my_file:
            c = csv.writer(my_file)
            for row in wb.rows:
                c.writerow([cell.value for cell in row])

    def ff_profile(self, download_dir):
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

    @retry(
        stop_max_attempt_number=7,
        stop_max_delay=30000,
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000
    )
    def _get_file_name(self, download_dir):
        """
        The file names below are examples of the raw data naming convention. 

        HIST_PAINEL_COVIDBR_21jun2020.xlsx
        HIST_PAINEL_COVIDBR_21jun2020.xlsx.part
        """
        target_files = list(download_dir.glob("HIST_PAINEL_COVIDBR*"))
        if len(target_files) == 1 and str(target_files[0]).endswith('.xlsx'):
            logger.info("Download complete")
            return str(target_files[0])
        if len(target_files) > 1:
            logger.info("Download not yet complete...")
            raise DownloadInProgressError
        else:
            raise Exception("Unexpected downloading condition encountered.")

    def _rename_xlxs(self, full_path):
        original = Path(full_path)
        new_name = original.parent.joinpath("{}.xlsx".format(self.runtimestamp))
        original.rename(new_name)
        return str(new_name)


    