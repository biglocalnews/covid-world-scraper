from bs4 import BeautifulSoup
import requests
import pandas as pd
from old_germany import move_data_ger

def india():

    url = 'https://www.mohfw.gov.in/'
    data = requests.get(url)

    soup = BeautifulSoup(data.text, 'html.parser')
        
    table = soup.table
    print(table)

    data_list = []
    headers = []
    table_row = table.find_all('tr')
    for tr in table_row:

        th = tr.find_all('th')
        for header in th:
            headers.append(header.text)

        td = tr.find_all('td')
        text_list = []
        for data in td:
            text_list.append(data.text)
        data_list.append(text_list)

    
    data_list = data_list[1:38]


    new_list = []
    for row in data_list:
        print(row)
        print(len(row))

        counter = 0
        for i in row:
            i = i.replace('\n', '')
            print(i)
            row[counter] = i
            counter += 1

    india_covid_df = pd.DataFrame(data_list, columns = headers)
    india_covid_df.to_csv('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/Data/india_covid19.csv', index=False)

    move_data_ger()

        

if __name__ == '__main__':
    india()