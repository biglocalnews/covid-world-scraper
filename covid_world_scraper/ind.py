"""
Official page for India COVID figures:

    https://www.mohfw.gov.in/

"""

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
            headers.extend(["date", "scrape_date"])
            data = []
            date = soup.find("div", class_="status-update")
            date = date.text.split(':', 1)[1]\
                .replace('\n', '')\
                .replace('\t', '')\
                .strip()
            scrape_date = self.runtimestamp
            try:
                tbody_rows = soup.table.tbody.find_all('tr')
            except AttributeError:
                # HACK due to apparent change in HTML table structure around July 27, 2020
                tbody_rows = self._extract_tbody_rows(soup)
            for tr in tbody_rows:
                cells = [cell.text.strip() for cell in tr.find_all('td')]
                if self._is_data_row(cells):
                    cells.extend([date, scrape_date])
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

    def _extract_tbody_rows(self, soup):
        # Transform into table row instances and return
        raw_text = soup.table.contents[3].replace('\n\t', '')
        soup = BeautifulSoup(raw_text, 'html.parser')
        return soup.find_all('tr')

    def _is_data_row(self, row):
        status = False
        if re.match(r'\d+', row[0]):
            status = True
        try:
            if re.match(r'^(Cases|Total).+$', row[1]):
                status = True
        except IndexError:
            # footnote lines are single-element lists
            pass
        return status

