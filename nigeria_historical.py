from bs4 import BeautifulSoup
from old_germany import move_data_ger
import requests
import pandas as pd
from pathlib import Path

def download_historical():

    url = 'https://ncdc.gov.ng/diseases/sitreps/?cat=14&name=An%20update%20of%20COVID-19%20outbreak%20in%20Nigeria'

    data = requests.get(url)

    soup = BeautifulSoup(data.text, 'html.parser')
    table = soup.table

    links_list = []
    dates_list = []
    url_base = 'https://ncdc.gov.ng/'

    table_row = table.find_all('tr')
    for tr in table_row:
        tr.find_all('a')
        for link in tr.find_all('a'):
            url_suffix = link.get('href')
            full_url = url_base + url_suffix
            links_list.append(full_url)

    counter = 0
    filename = Path('/Users/dilcia_mercedes/Desktop/historical_data/nigeria.pdf')
    # print(links_list)
    
    for link in links_list:

        new_data = requests.get(link)
        filename.write_bytes(new_data.content)
        
        # with open('/Users/dilcia_mercedes/Desktop/historical_data/nigeria_' + str(counter) + '.pdf', 'w') as pdf_file:
        #     pdf_file.write_bytes(new_data.content)
        counter += 1


if __name__ == '__main__':
    download_historical()