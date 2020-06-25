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

        covid_deaths_list = []
        covid_cases_list = []

        with open(source_file) as html_file:
            soup = BeautifulSoup(html_file.read(), 'html.parser')

            date = soup.find("span", class_="updated rich-snippet-hidden")
            scrape_date = self.runtimestamp

            # Extracting cases data 
            tables = soup.find_all('table')
            covid_cases = tables[0]

            covid_table_row = covid_cases.find_all('tr')
            for tr in covid_table_row:
                cells = [
                    cell.text.strip().replace(',','.')
                    for cell in tr.find_all('td')
                ]
                cells.extend([date.text])
                cells.extend([scrape_date])
                covid_cases_list.append(cells)


            # Extracting deaths data
            covid_deaths = tables[1]
            deaths_table_row = covid_deaths.find_all('tr')
            for tr in deaths_table_row:
                cells = [
                    cell.text.strip().replace(',','.')
                    for cell in tr.find_all('td')
                ]

                cells.extend([date.text])
                cells.extend([scrape_date])
                covid_deaths_list.append(cells)

            
            covid_cases_list[0][3] = "Date"
            covid_cases_list[0][4] = "Scrape_Date"
            covid_deaths_list[0][3] = "Date"
            covid_deaths_list[0][4] = "Scrape_Date"

        cases_headers = covid_cases_list[0]
        cases_list = covid_cases_list[1:]
        deaths_headers = covid_deaths_list[0]
        deaths_list = covid_deaths_list[1:]

        processed_base_name = source_file.split('.')[0]
        cases_outfile = '{}_cases.csv'.format(processed_base_name)
        merged_case_data = [cases_headers]
        merged_case_data.extend(cases_list)
        self.write_csv(merged_case_data, cases_outfile)

        deaths_outfile = '{}_deaths.csv'.format(processed_base_name)
        merged_deaths_data = [deaths_headers]
        merged_deaths_data.extend(deaths_list)
        self.write_csv(merged_deaths_data, deaths_outfile)

        return cases_outfile, deaths_outfile

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

