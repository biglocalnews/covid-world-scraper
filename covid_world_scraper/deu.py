"""
Official page for Germany COVID figures:

    https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html

"""
import csv
import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from .country_scraper import CountryScraper

logger = logging.getLogger(__name__)

class Deu(CountryScraper):

    def fetch(self):
        url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
        opts = Options()
        opts.headless = True
        data = []
        try:
            driver = webdriver.Firefox(options=opts)
            driver.get(url)
            driver.get_screenshot_as_file(self._screenshot_path)
            logger.info("Saved screenshot of web page to {}".format(self._screenshot_path))
            table = driver.find_element_by_tag_name("table")
            inner_html = table.get_attribute('innerHTML')
            inner_text = table.get_attribute('innerText')
            cached_html_path = self.save_to_raw_cache(inner_html, 'html')
            cached_text_path = self.save_to_raw_cache(inner_text, 'txt')
        finally:
            driver.quit()
        return cached_text_path

    def extract(self, source_file):
        deu_data = []
        with open(source_file, 'r') as infile:
            for line in infile:
                line = line.replace('\xad', '')
                line = line.replace('Vorpommern', 'Mecklenburg-Vorpommern')
                line = line.replace('Gesamt', 'Total')
                line = line.split()
                if len(line) > 4:
                    deu_data.append(line)

            for item in deu_data:
                item[1] = item[1].replace('.','')
                item[1] = int(item[1])
                item[2] = item[2].replace('+','')
                item[2] = int(item[2])
                item[3] = float(item[3])
                item[4] = item[4].replace(',','.')
                item[4] = float(item[4])
                item[5] = int(item[5].replace('.',''))
                
        basename = source_file.split('/')[-1].replace('txt','csv')
        outfile = str(self.processed_dir.joinpath(basename))
        self._write_csv(deu_data, outfile)
        logger.info('Created {}'.format(outfile))
        return outfile


    def _write_csv(self, data, outfile):

        header = [
            'Federal State', 
            'Number of Cases', 
            'Difference from Prior Day', 
            'Cases in past 7 Days', 
            '7-day Incidence', 
            'Deaths'
            ]

        with open(outfile,'w') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            writer.writerows(data)
        logger.info("Save extracted data to {}".format(outfile))