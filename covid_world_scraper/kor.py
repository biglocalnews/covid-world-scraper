"""
Official page for South Korea COVID figures:

    http://ncov.mohw.go.kr/en/bdBoardList.do?brdId=16&brdGubun=162&dataGubun=&ncvContSeq=&contSeq=&board_id=&gubun=

"""
from datetime import datetime
import logging
import os
import re

from bs4 import BeautifulSoup
import requests

from .country_scraper import CountryScraper
from .utils import relative_year


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
            date = soup.find_all("font")
            scrape_date = self.runtimestamp
            data = []
            headers = [
                "City/Province",
                "Daily Change",
                "Imported Cases",
                "Local Outbreak",
                "Confirmed Cases",
                "Isolated",
                "Released from Quarantine",
                "Deceased",
                "Incidence(*)",
                "date",
                "scrape_date"
            ]
            raw_date = soup.find("p", class_="info")
            site_date = self._parse_date(raw_date.text)
            scrape_date = self.runtimestamp
            tbody_rows = soup.table.tbody.find_all('tr')
            for tr in tbody_rows:
                province = tr.th.text.strip()
                cells = [
                    cell.text.strip().replace(',','')
                    for cell in tr.find_all('td')
                ]
                all_data = [province]
                all_data.extend(cells)
                all_data.extend([site_date, self.runtimestamp])
                data.append(all_data)
        outfile = self.processed_filepath_from_raw(raw_data_path, 'csv')
        merged_data = [headers]
        merged_data.extend(data)
        self.write_csv(merged_data, outfile)
        return outfile

    def _parse_date(self, date):
        pattern = r'.+\s(\d+)(am|pm)\s+([\d.]+)'
        hour, meridian, month_day = re.match(
            pattern, date.strip()
        ).groups()
        hour_clean = int(hour)
        month, day = [int(bit) for bit in month_day.rstrip('.').split('.')[0:2]]
        meridian_clean = meridian.strip().lower()
        if hour_clean == 12:
            hour_clean = 0
        if meridian_clean == 'pm':
            hour_clean += 12
        year = relative_year(month, day)
        dt = datetime(year, month, day, hour_clean, 0)
        return dt.strftime("%Y%m%dT%H%S")
