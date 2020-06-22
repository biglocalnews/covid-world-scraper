from bs4 import BeautifulSoup
# from old_germany import move_data_ger
import requests
import os
import pandas as pd

def nigeria():

    url = 'https://covid19.ncdc.gov.ng/'
    data = requests.get(url)

    soup = BeautifulSoup(data.text, 'html.parser')
    
    table = soup.table
    
    data_list = []
    headers = []
    table_row = table.find_all('tr')
    
    for tr in table_row:

        th = tr.find_all('th')
        for header in th:
            headers.append(header.text)

        text_list = []
        td = tr.find_all('td')
        for data in td:
            text_list.append(data.text)
        data_list.append(text_list)

    data_list = data_list[1:]
    
    for data_row in data_list:
        counter = 0
        for data in data_row:
            data = data.replace('\n', '')
            data_row[counter] = data
            counter += 1


    
    nigeria_covid_df = pd.DataFrame(data_list, columns = headers)
    file_name = 'nigeria_covid19.csv'
    base_path = os.environ['TO_DATA_DIR']
    full_path = f'{base_path}/{file_name}'

    nigeria_covid_df.to_csv(full_path, index=False)

    # nigeria_covid_df.to_csv('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/Data/nigeria_covid19.csv', index=False)

    # move_data_ger()
    


if __name__ == '__main__':
    nigeria()