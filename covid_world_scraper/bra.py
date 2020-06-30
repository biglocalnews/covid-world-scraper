import csv
import logging
import os
import openpyxl
from pathlib import Path

from retrying import retry
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .country_scraper import CountryScraper

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

        wb = openpyxl.load_workbook(raw_data_path)
        sh = wb.get_active_sheet()
        with open('test.csv', 'wb') as my_file:
            c = csv.writer(my_file)
            for row in sh.rows:
                c.writerow([cell.value for cell in row])

    