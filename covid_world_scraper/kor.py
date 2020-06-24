"""
Official page for South Korea COVID figures:

    http://ncov.mohw.go.kr/en/bdBoardList.do?brdId=16&brdGubun=162&dataGubun=&ncvContSeq=&contSeq=&board_id=&gubun=

"""

import logging
import os
import re

from bs4 import BeautifulSoup
import requests

from .country_scraper import CountryScraper


logger = logging.getLogger(__name__)

class Kor(CountryScraper):

    def fetch(self):
        url = 'http://ncov.mohw.go.kr/en/bdBoardList.do?brdId=16&brdGubun=162&dataGubun=&ncvContSeq=&contSeq=&board_id=&gubun='
        response = requests.get(url)
        saved_file = self.save_to_raw_cache(response.text, 'html')
        return saved_file


    def extract(self, raw_data_path):
        with open(raw_data_path) as fh:
            soup = BeautifulSoup(fh.read(), 'html.parser')
            data = []
            headers = ["City/Province", "Daily Change", "Imported Cases", "Local Outbreak", "Confirmed Cases", "Isolated", "Released from Quarantine", "Deceased", "Incidence(*)"]
            tbody_rows = soup.table.tbody.find_all('tr')
            for tr in tbody_rows:
                provinces = [cell.text.strip() for cell in tr.find_all('th')]
                cells = [cell.text.strip() for cell in tr.find_all('td')]
                for province, cell in zip(provinces, cells):
                    all_data = [province]
                    all_data.extend(cells)
                data.append(all_data)
         
        outfile = self.processed_filepath_from_raw(raw_data_path, 'csv')
        merged_data = [headers]
        merged_data.extend(data)
        self.write_csv(merged_data, outfile)
        return outfile

        
