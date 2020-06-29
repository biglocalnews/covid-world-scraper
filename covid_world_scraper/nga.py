"""
Official page for Nigeria COVID figures:

    https://covid19.ncdc.gov.ng/

"""
import logging
import os
import re

from bs4 import BeautifulSoup
import requests

from .country_scraper import CountryScraper

logger = logging.getLogger(__name__)

class Nga(CountryScraper):

    def fetch(self):

        url = 'https://covid19.ncdc.gov.ng/'
        response = requests.get(url)
        saved_file = self.save_to_raw_cache(response.text, 'html')
        return saved_file

    def extract(self, source_file):

        scrape_date = self.runtimestamp

        with open(source_file) as fh:
            soup = BeautifulSoup(fh.read(), 'html.parser')
            headers = [h.text for h in soup.table.thead.find_all('th')]
            headers.extend(['date', 'scrape_date'])
            data = []

            tbody_rows = soup.table.tbody.find_all('tr')
            for tr in tbody_rows:
                cells = [cell.text.strip() for cell in tr.find_all('td')]
                cells.extend(['', scrape_date])
                data.append(cells)

        outfile = self.processed_filepath_from_raw(source_file, 'csv')
        merged_data = [headers]
        merged_data.extend(data)
        self.write_csv(merged_data, outfile)
        return outfile