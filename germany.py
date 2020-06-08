from bs4 import BeautifulSoup
import requests
import pandas as pd

def germany():

    output_header = ['Federal State', 'Number of Cases', 'Difference from Prior Day', 'Cases in past 7 Days', '7-day Incidence', 'Deaths']

    url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html'
    data = requests.get(url)

    soup = BeautifulSoup(data.text, 'html.parser')

    table = soup.table

    data_list = []
    table_row = table.find_all('tr')
    for tr in table_row:

        td = tr.find_all('td')
        text_list = []
        for data in td:
            text_list.append(data.text)
        data_list.append(text_list)

        print('')

    
    data_list = data_list[2:]
    new_list = []
    for row in data_list:
        print(row)
        print(len(row))

        counter = 0
        for i in row:
            i = i.replace('\xad', '')
            i = i.replace('\n', '')
            if i == 'Gesamt':
                i = 'Total'
            print(i)
            row[counter] = i
            counter += 1


    df = pd.DataFrame(data_list, columns = output_header)
    df['Number of Cases'] = df['Number of Cases'].str.replace('.', ',')
    df['Cases in past 7 Days'] = df['Cases in past 7 Days'].str.replace('.', ',')
    df['7-day Incidence'] = df['7-day Incidence'].str.replace(',', '.')
    df['Deaths'] = df['Deaths'].str.replace('.', ',')
    print(df)

    df.to_csv('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/Data/germany_covid19.csv', index=False)


if __name__ == '__main__':
    germany()