"""
Official page for Germany COVID figures:

    https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html

"""
import logging
import os
import re

from bs4 import BeautifulSoup
import requests

from .country_scraper import CountryScraper

logger = logging.getLogger(__name__)

class Deu(CountryScraper):

    def fetch(self):

        url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
        response = requests.get(url)
        saved_file = self.save_to_raw_cache(response.text, 'html')
        return saved_file

    def extract(self, raw_data_path):
        with open(raw_data_path) as fh:
            soup = BeautifulSoup(fh.read(), 'html.parser')
            date = soup.find_all("p")[11].text
            scrape_date = self.runtimestamp
            header = [
                'Federal State', 
                'Number of Cases', 
                'Difference from Prior Day', 
                'Cases in past 7 Days', 
                '7-day Incidence', 
                'Deaths',
                'date',
                'scrape_date'
                ]
            table = soup.table

            data_list = []
            table_row = table.find_all('tr')
            for tr in table_row:
                td = tr.find_all('td')
                text_list = []
                for data in td:
                    text_list.append(data.text)
                data_list.append(text_list)

            data_list = data_list[2:]

            for row in data_list:
                counter = 0
                for i in row:
                    i = i.replace('\xad', '')
                    i = i.replace('\n', '')
                    i = i.replace('Gesamt', 'Total')
            
                    row[counter] = i
                    counter += 1

    
            for item in data_list:

                item[1] = item[1].replace('.','')
                item[1] = int(item[1])
                item[2] = item[2].replace('+','')
                item[2] = item[2].replace('*','')
                item[2] = int(item[2])
                item[3] = float(item[3])
                item[4] = item[4].replace(',','.')
                item[4] = float(item[4])
                item[5] = int(item[5].replace('.',''))
                item.extend([date, scrape_date])


        outfile = self.processed_filepath_from_raw(raw_data_path, 'csv')
        merged_data = [header]
        merged_data.extend(data_list)
        self.write_csv(merged_data, outfile)
        return outfile

