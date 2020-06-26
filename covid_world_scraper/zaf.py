"""
Official page for South Africa COVID figures:

    https://sacoronavirus.co.za/category/press-releases-and-notices/

"""
import logging
import os
import re
import time
from datetime import datetime

from bs4 import BeautifulSoup
import requests

from .country_scraper import CountryScraper


logger = logging.getLogger(__name__)


class Zaf(CountryScraper):

    def fetch(self):
        orig_url = 'https://sacoronavirus.co.za/category/press-releases-and-notices/'
        orig_page = requests.get(orig_url)
        soup = BeautifulSoup(orig_page.text, 'html.parser')
        data_links = self._data_page_links(soup)
        most_recent_link = data_links[0][1]
        page = requests.get(most_recent_link)
        saved_file = self.save_to_raw_cache(page.text, 'html')
        return saved_file

    def extract(self, source_file):
        with open(source_file) as html_file:
            soup = BeautifulSoup(html_file.read(), 'html.parser')
            date = soup.find("span", class_="updated rich-snippet-hidden")
            scrape_date = self.runtimestamp
            # Extracting cases data
            tables = soup.find_all('table')
            cases = self._prepare_processed_csv(tables[0], date, scrape_date)
            deaths = self._prepare_processed_csv(tables[1], date, scrape_date)

        # Generate output fiel names
        processed_base_name = source_file.split('.')[0]
        cases_outfile = '{}_cases.csv'.format(processed_base_name)
        deaths_outfile = '{}_deaths.csv'.format(processed_base_name)

        # Write data
        self.write_csv(cases, cases_outfile)
        self.write_csv(deaths, deaths_outfile)

        return cases_outfile, deaths_outfile

    def _prepare_processed_csv(self, table, date, scrape_date):
        # Add date fields to header rows
        data = []
        for tr in table.find_all('tr'):
            cells = [
                cell.text.strip().replace(',','.')
                for cell in tr.find_all('td')
            ]
            cells.extend([date.text, scrape_date])
            data.append(cells)
        # Add new fields to header row
        data[0].extend(['date', 'scrape_date'])
        return data

    def _data_page_links(self, soup):
        # Grab all links
        links = soup.find_all('a')
        # Then filter for date page links.
        # Along the way, convert day, month and year to numbers.
        # Create a tuple (year, month, day) and
        # store the date tuple and link to date page in data_links
        data_links = []
        for link in links:
            try:
                href = link['href']
                if 'update-on-covid-19' in href:
                    pattern = r'update-on-covid-19-(\d{1,2}).+-(.+)-(\d{4})/'
                    day, month, year =  re.search(pattern, href).groups()
                    key = (
                        int(year),
                        datetime.strptime(month, '%B').month,
                        int(day)
                    )
                    data_links.append([key, href])
            except KeyError:
                # Some links have no 'href' attribute
                pass
        # Sort links from most recent to farthest back
        return sorted(
            data_links,
            key=lambda x: x[0],
            reverse=True
        )

