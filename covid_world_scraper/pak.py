"""
Official page for Pakistan COVID figures:

    http://covid.gov.pk/stats/pakistan

"""
import csv
import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .country_scraper import CountryScraper


logger = logging.getLogger(__name__)


class Pak(CountryScraper):

    ## Standard method overrides
    def fetch(self):
        url = "https://datastudio.google.com/embed/reporting/1PLVi5amcc_R5Gh928gTE8-8r8-fLXJQF/page/R24IB"
        opts = Options()
        opts.headless = True
        data = []
        try:
            driver = webdriver.Firefox(options=opts)
            driver.get(url)
            # Gross, but works
            time.sleep(20)
            driver.get_screenshot_as_file(self._screenshot_path)
            logger.info("Saved screenshot of web page to {}".format(self._screenshot_path))
            date = driver.find_elements_by_xpath('/html/body/app-bootstrap/ng2-bootstrap/bootstrap/div/div/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/div/lego-report/lego-canvas-container/div/file-drop-zone/span/content-section/canvas-component[20]/div/div/div[1]/div/div/lego-table/div/div[3]/div/div')[0].get_attribute('innerText')
            scrape_date = self.runtimestamp

            tables = driver.find_elements_by_css_selector('lego-table.table.ng-scope')
            for tbl in tables:
                text = tbl.text.strip().replace(',','')
                if text.startswith('AJK'):
                    inner_html = tbl.get_attribute('innerHTML')
                    inner_text = tbl.get_attribute('innerText')
                    cached_html_path = self.save_to_raw_cache(inner_html, 'html')
                    cached_text_path = self.save_to_raw_cache(inner_text, 'txt')
        finally:
            driver.quit()
        return cached_text_path, date, scrape_date

    def extract(self, source_file):
        with open(source_file, 'r') as infile:
            text = infile.read().replace(',','')
            data = self._chunks(text.split('\n'))
            basename = source_file.split('/')[-1].replace('txt','csv')
            outfile = str(self.processed_dir.joinpath(basename))
            self._write_csv(data, outfile)
            return outfile

    ## PRIVATE ##

    def _write_csv(self, data, outfile):
        header = [
            'admin_unit',
            'confirmed_cases',
            'active_cases',
            'deaths',
            'recoveries'
        ]
        with open(outfile,'w') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            writer.writerows(data)
        logger.info("Save extracted data to {}".format(outfile))

    def _chunks(self, lst):
        chunk_size = 5
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]
