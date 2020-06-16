import datetime
import os
import pandas as pd
from get_historical_data import files_list

def germany_combine():

    # grabs germany files ordered by date
    # most recent to least recent data

    germany_files = files_list('germany')
    
    path = '/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/old_data'

    headers = ['Province/State', 'Country/Region']
    germany_covid_cases = pd.DataFrame(columns = headers)
    germany_covid_deaths = pd.DataFrame(columns = headers)

    for file in germany_files:

        # combining data from all files for given country

        full_path = f'{path}/{file}'
        file = file[0:10].split('-')
        month_day_year = f'{file[1]}/{file[2]}/{file[0]}'

        read_file = pd.read_csv(full_path)
        read_file = read_file.iloc[: -1, :] # dropping totals column

        germany_covid_cases['Province/State'] = read_file['Federal State']
        germany_covid_cases[month_day_year] = read_file['Number of Cases']
        germany_covid_cases['Country/Region'] = 'Germany'

        germany_covid_deaths['Province/State'] = read_file['Federal State']
        germany_covid_deaths[month_day_year] = read_file['Deaths']
        germany_covid_deaths['Country/Region'] = 'Germany'

    # print(germany_covid_deaths)
    cases_file = germany_covid_cases.to_csv(f'/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/aggregated_data/germany_covid_cases.csv')
    deaths_file = germany_covid_deaths.to_csv(f'/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/aggregated_data/germany_covid_deaths.csv')




if __name__ == '__main__':
    germany_combine()