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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

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
                

        covid_cases_header = covid_cases_list[0]
        covid_cases_list = covid_cases_list[1:]
        covid_deaths_header = covid_deaths_list[0]
        covid_deaths_list = covid_deaths_list[1:]

        basename = source_file.split('/')[-1].replace('.html','_cases.csv')
        cases_outfile = str(self.processed_dir.joinpath(basename))
        self._write_csv(covid_cases_header, covid_cases_list, cases_outfile)
        logger.info('Created {}'.format(cases_outfile))

        deaths_basename = source_file.split('/')[-1].replace('.html','_deaths.csv')
        deaths_outfile = str(self.processed_dir.joinpath(deaths_basename))
        self._write_csv(covid_deaths_header, covid_deaths_list, deaths_outfile)
        logger.info('Created {}'.format(deaths_outfile))

        return cases_outfile, deaths_outfile


    def _write_csv(self, header, data, outfile):

        with open(outfile,'w') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            writer.writerows(data)
        logger.info("Save extracted data to {}".format(outfile))
