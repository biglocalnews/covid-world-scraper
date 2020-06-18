from bs4 import BeautifulSoup
from datetime import date
import requests
import os
import pandas as pd


def spain():

    today_date = date.today()

    url = 'https://www.mscbs.gob.es/profesionales/saludPublica/ccayes/alertasActual/nCov-China/situacionActual.htm'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    data_element = soup.find_all("li")[28]
    href = data_element.find("a")
    link = href.get("href")
    base_url = 'https://www.mscbs.gob.es/'
    new_link = link.rsplit('..', 1)[1]
    full_url = f'{base_url}{new_link}'

    page_2 = requests.get(full_url, stream=True)
    file_name = f'{today_date}_spain_covid19.pdf'
    base_path = os.environ['TO_PDF_DIR']
    full_path = f'{base_path}/{file_name}'

    with open(full_path, 'wb') as cov_pdf:
        for chunk in page_2.iter_content(chunk_size=128):
            cov_pdf.write(chunk)



if __name__ == '__main__':
    spain()