from bs4 import BeautifulSoup
from old_germany import move_data_ger
import requests
import pandas as pd


def south_africa():

    orig_url = 'https://sacoronavirus.co.za/category/press-releases-and-notices/'
    orig_page = requests.get(orig_url)

    soup = BeautifulSoup(orig_page.text, 'html.parser')
    div = soup.find("div", class_="fusion-rollover")
    link_tag = div.find("a")
    link = link_tag.get("href")
    
    page = requests.get(link)
    new_soup = BeautifulSoup(page.text, 'html.parser')
    tables = new_soup.find_all('table')
    covid_cases = tables[0]
    covid_deaths = tables[1]
    
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

    remove_base = link.split('https://sacoronavirus.co.za/')
    half_link = remove_base[1].split('/update')
    date = half_link[0]
    parsed_date = date.split('/')
    year = parsed_date[0]
    month = parsed_date[1]
    day = parsed_date[2]
    print(parsed_date)
    print(link)

    SA_cases_df.to_csv(f'/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/Data/{year}-{month}-{day}_south_africa_covid19.csv', index=False)
    SA_deaths_df.to_csv(f'/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/Data/{year}-{month}-{day}_south_africa_covid19_deaths.csv', index=False)

    move_data_ger()


if __name__ == '__main__':
    south_africa()

