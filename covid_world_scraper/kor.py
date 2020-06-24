"""
Official page for South Korea COVID figures:

    http://ncov.mohw.go.kr/en/bdBoardList.do?brdId=16&brdGubun=162&dataGubun=&ncvContSeq=&contSeq=&board_id=&gubun=

"""

import csv
import logging
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from .country_scraper import CountryScraper

logger = logging.getLogger(__name__)

headers = ["City/Province", "Daily Change", "Imported Cases", "Local Outbreak", "Confirmed Cases", "Isolated", "Released from Quarantine", "Deceased", "Incidence(*)"]

class Kor(CountryScraper):

    def fetch(self):
        url = 'http://ncov.mohw.go.kr/en/bdBoardList.do?brdId=16&brdGubun=162&dataGubun=&ncvContSeq=&contSeq=&board_id=&gubun='
        opts = Options()
        opts.headless = True
        try:
            driver = webdriver.Firefox(options=opts)
            driver.get(url)
            driver.get_screenshot_as_file(self._screenshot_path)
            logger.info("Saved screenshot of web page to {}".format(self._screenshot_path))
            table = driver.find_element_by_tag_name("table")
            inner_html = table.get_attribute('innerHTML')
            inner_text = table.get_attribute('innerText')
            cached_html_path = self.save_to_raw_cache(inner_html, 'html')
            cached_text_path = self.save_to_raw_cache(inner_text, 'txt')
        finally:
            driver.quit()
        return cached_text_path


    def extract(self, source_file):

        kor_data = []
        kor_data_updated = []
        with open(source_file, 'r') as infile:
            for line in infile:
                kor_data.append(line)

        kor_data = kor_data[3:]
        
        for row in kor_data:
            row = row.split("\t")
            row[-1] = row[-1].strip()
            # row = row.replace(",", "")
            kor_data_updated.append(row)

        print(kor_data_updated)

        
