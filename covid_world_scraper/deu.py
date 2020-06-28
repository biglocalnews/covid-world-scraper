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
            data = []
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

            new_list = []
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
                item[2] = int(item[2])
                item[3] = float(item[3])
                item[4] = item[4].replace(',','.')
                item[4] = float(item[4])
                item[5] = int(item[5].replace('.',''))


        outfile = self.processed_filepath_from_raw(raw_data_path, 'csv')
        merged_data = [header]
        merged_data.extend(data_list)
        self.write_csv(merged_data, outfile)
        return outfile



          
            

        # url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
        # opts = Options()
        # opts.headless = True
        # data = []
        # try:
        #     driver = webdriver.Firefox(options=opts)
        #     driver.get(url)
        #     driver.get_screenshot_as_file(self._screenshot_path)
        #     logger.info("Saved screenshot of web page to {}".format(self._screenshot_path))
        #     table = driver.find_element_by_tag_name("table")
        #     inner_html = table.get_attribute('innerHTML')
        #     inner_text = table.get_attribute('innerText')
        #     cached_html_path = self.save_to_raw_cache(inner_html, 'html')
        #     cached_text_path = self.save_to_raw_cache(inner_text, 'txt')
        # finally:
        #     driver.quit()
        # return cached_text_path

    # def extract(self, source_file):
    #     deu_data = []
    #     with open(source_file, 'r') as infile:
    #         for line in infile:
    #             line = line.replace('\xad', '')
    #             line = line.replace('Vorpommern', 'Mecklenburg-Vorpommern')
    #             line = line.replace('Gesamt', 'Total')
    #             line = line.split()
    #             if len(line) > 4:
    #                 deu_data.append(line)

    #         for item in deu_data:
    #             item[1] = item[1].replace('.','')
    #             item[1] = int(item[1])
    #             item[2] = item[2].replace('+','')
    #             item[2] = int(item[2])
    #             item[3] = float(item[3])
    #             item[4] = item[4].replace(',','.')
    #             item[4] = float(item[4])
    #             item[5] = int(item[5].replace('.',''))
                
    #     basename = source_file.split('/')[-1].replace('txt','csv')
    #     outfile = str(self.processed_dir.joinpath(basename))
    #     self._write_csv(deu_data, outfile)
    #     logger.info('Created {}'.format(outfile))
    #     return outfile


    # def _write_csv(self, data, outfile):

    #     header = [
    #         'Federal State', 
    #         'Number of Cases', 
    #         'Difference from Prior Day', 
    #         'Cases in past 7 Days', 
    #         '7-day Incidence', 
    #         'Deaths'
    #         ]

    #     with open(outfile,'w') as out:
    #         writer = csv.writer(out)
    #         writer.writerow(header)
    #         writer.writerows(data)
    #     logger.info("Save extracted data to {}".format(outfile))