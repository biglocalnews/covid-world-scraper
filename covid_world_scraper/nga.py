"""
Official page for Nigeria COVID figures:

    https://covid19.ncdc.gov.ng/

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

class Nga(CountryScraper):

    def fetch(self):

        url = 'https://covid19.ncdc.gov.ng/'
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

        nga_header = []
        nga_data = []
        with open(source_file, 'r') as infile:
            for line in infile:
                if 'States Affected' in line:
                    line = line.replace('\n', '')
                    line = line.split('\t')
                    nga_header.append(line)
                else:
                    line = line.replace(',','')
                    line = line.split()
                    if len(line) > 5:
                        line[0] = f'{line[0]} {line[1]}'
                        line.pop(1)
                    nga_data.append(line)

            
            for row in nga_data:
                counter = 0
                for item in row:
                    if item.isnumeric():
                        item = int(item)
                        row[counter] = item
                        counter += 1
                    else:
                        item = str(item)
                        row[counter] = item
                        counter += 1

        basename = source_file.split('/')[-1].replace('txt','csv')
        outfile = str(self.processed_dir.joinpath(basename))
        self._write_csv(nga_header, nga_data, outfile)
        logger.info('Created {}'.format(outfile))
        return outfile


    def _write_csv(self, header, data, outfile):

        with open(outfile,'w') as out:
            writer = csv.writer(out)
            writer.writerow(header[0])
            writer.writerows(data)
        logger.info("Save extracted data to {}".format(outfile))

    
