import logging
import os
import re

from bs4 import BeautifulSoup
import requests


logger = logging.getLogger(__name__)


from .country_scraper import CountryScraper


class Ind(CountryScraper):


    def fetch(self):
        url = 'https://www.mohfw.gov.in/'
        response = requests.get(url)
        saved_file = self.save_to_raw_cache(response.text, 'html')
        return saved_file

    def extract(self, raw_data_path):
        with open(raw_data_path) as fh:
            soup = BeautifulSoup(fh.read(), 'html.parser')
            headers = [h.text for h in soup.table.thead.find_all('th')]
            data = []
            tbody_rows = soup.table.tbody.find_all('tr')
            for tr in tbody_rows:
                cells = [cell.text.strip() for cell in tr.find_all('td')]
                if self._is_data_row(cells):
                    data.append(cells)
                else:
                    # footnote cells at bottom of table
                    # signal end of relevant data, so
                    # break to avoid extra loops
                    break
        outfile = self.processed_filepath_from_raw(raw_data_path, 'csv')
        merged_data = [headers]
        merged_data.extend(data)
        self.write_csv(merged_data, outfile)
        return outfile

    def _is_data_row(self, row):
        return re.match(r'\d+', row[0])

