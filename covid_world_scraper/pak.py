"""
Official page for Pakistan COVID figures:

    http://covid.gov.pk/stats/pakistan

"""
import csv
import logging
import os
import re
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
        opts.headless = self.headless_status
        data = []
        try:
            driver = webdriver.Firefox(options=opts)
            driver.get(url)
            #TODO: Replace with a wait statement that
            # ensures timestamp has appeared on page
            time.sleep(30)
            driver.get_screenshot_as_file(self._screenshot_path)
            logger.info("Saved screenshot of web page to {}".format(self._screenshot_path))
            scrape_date = self.runtimestamp
            date = ''
            tables = driver.find_elements_by_css_selector('lego-table.table.ng-scope')
            for tbl in tables:
                text = tbl.text.strip().replace(',','')
                if text.startswith('Last updated on'):
                    date = text.replace('\n',' ')
                if text.startswith('AJK'):
                    inner_html = tbl.get_attribute('innerHTML')
                    inner_text = tbl.get_attribute('innerText')
                    cached_html_path = self.save_to_raw_cache(inner_html, 'html')
                    cached_text_path = self.save_to_raw_cache(inner_text, 'txt')
        finally:
            driver.quit()
        return {
            'cached_text_path': cached_text_path,
            'date': date,
            'scrape_date': scrape_date,
        }

    def extract(self, payload):
        source_file = payload['cached_text_path']
        date = payload['date']
        scrape_date = payload['scrape_date']
        with open(source_file, 'r') as infile:
            text = infile.read().replace(',','')
            data = []
            for row in self._chunks(text.split('\n')):
                row.extend([date, scrape_date])
                data.append(row)
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
            'recoveries',
            'date',
            'scrape_date',
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
