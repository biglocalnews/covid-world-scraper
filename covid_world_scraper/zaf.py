"""
Official page for South Africa COVID figures:

    https://sacoronavirus.co.za/category/press-releases-and-notices/

"""
import csv
import logging
import os
import requests
import time

from bs4 import BeautifulSoup

from .country_scraper import CountryScraper

logger = logging.getLogger(__name__)

class Zaf(CountryScraper):

    def fetch(self):

        orig_url = 'https://sacoronavirus.co.za/category/press-releases-and-notices/'
        orig_page = requests.get(orig_url)

        soup = BeautifulSoup(orig_page.text, 'html.parser')
        div = soup.find("div", class_="fusion-rollover")
        link_tag = div.find("a")
        link = link_tag.get("href")

        #replacing above for now
        link = 'https://sacoronavirus.co.za/2020/06/23/update-on-covid-19-23rd-june-2020/'

        page = requests.get(link)
        saved_file = self.save_to_raw_cache(page.text, 'html')
        return saved_file

    def extract(self, source_file):

        covid_deaths_list = []
        covid_cases_list = []

        with open(source_file) as html_file:
            soup = BeautifulSoup(html_file.read(), 'html.parser')

            # Extracting cases data 

            tables = soup.find_all('table')
            covid_cases = tables[0]

            covid_table_row = covid_cases.find_all('tr')
            for tr in covid_table_row:

                text_list = []
                td = tr.find_all('td')
                for data in td:
                    text_list.append(data.text)
                covid_cases_list.append(text_list)

            # Extracting deaths data

            tables = soup.find_all('table')
            covid_deaths = tables[1]

            deaths_table_row = covid_deaths.find_all('tr')
            for tr in deaths_table_row:
                text_list = []
                td = tr.find_all('td')
                for data in td:
                    text_list.append(data.text)
                covid_deaths_list.append(text_list)
                

        cases_headers = covid_cases_list[0]
        cases_list = covid_cases_list[1:]
        deaths_headers = covid_deaths_list[0]
        deaths_list = covid_deaths_list[1:]

        cases_outfile = self.processed_filepath_from_raw(f'{source_file}_cases', 'csv')
        merged_data = [cases_headers]
        merged_data.extend(cases_list)
        self.write_csv(merged_data, cases_outfile)

        deaths_outfile = self.processed_filepath_from_raw(f'{source_file}_deaths', 'csv')
        merged_data = [deaths_headers]
        merged_data.extend(deaths_list)
        self.write_csv(merged_data, deaths_outfile)

        return cases_outfile, deaths_outfile