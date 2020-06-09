from bs4 import BeautifulSoup
import requests
import pandas as pd

def south_africa():

    url = 'https://www.nicd.ac.za/covid-19-update-3-jun/'
    data = requests.get(url)

    soup = BeautifulSoup(data.text, 'html.parser')
    tables = soup.find_all('table')
    covid_cases = tables[0]
    covid_deaths = tables[2]
    
    covid_cases_list = []

    covid_table_row = covid_cases.find_all('tr')
    for tr in covid_table_row:

        text_list = []
        td = tr.find_all('td')
        for data in td:
            text_list.append(data.text)
        covid_cases_list.append(text_list)

    covid_cases_header = covid_cases_list[0]
    covid_cases_list = covid_cases_list[1:]


    covid_deaths_list = []
    deaths_table_row = covid_deaths.find_all('tr')
    for tr in deaths_table_row:
        text_list = []
        td = tr.find_all('td')
        for data in td:
            text_list.append(data.text)
        covid_deaths_list.append(text_list)

    covid_deaths_header = covid_deaths_list[0]
    covid_deaths_list = covid_deaths_list[1:]

    SA_cases_df = pd.DataFrame(covid_cases_list, columns = covid_cases_header)
    SA_deaths_df = pd.DataFrame(covid_deaths_list, columns = covid_deaths_header)

    SA_cases_df['Percentage total'] = SA_cases_df['Percentage total'].str.replace(',', '.')

    SA_cases_df.to_csv('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/Data/south_africa_covid19.csv', index=False)
    SA_deaths_df.to_csv('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/Data/south_africa_covid19_deaths.csv', index=False)
    


if __name__ == '__main__':
    south_africa()