import datetime
import os
import pandas as pd
from pitch_last7 import get_last_seven

date = datetime.datetime.now()
year = date.year
day = date.day
month = date.month
month = str(month).zfill(2)
day = str(day).zfill(2)


date_input = f'{month}_{day}'

hi = get_last_seven(date_input)
# print(hi)

path = '/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/old_data'

headers = ['Province/State', 'Country/Region']
germany_covid_cases = pd.DataFrame(columns = headers)
germany_covid_deaths = pd.DataFrame(columns = headers)

# month_day_year_all = f'{month}/{day}/{year}'

for file in hi:

    full_file = f'{path}/{file}_germany_covid19.csv'

    file = file.split('-')
    month_day_year = f'{file[1]}/{file[2]}/{file[0]}'
    read_file = pd.read_csv(full_file)
    read_file = read_file.iloc[: -1, :] # dropping totals column

    # print(read_file.columns)

    germany_covid_cases['Province/State'] = read_file['Federal State']
    germany_covid_cases[month_day_year] = read_file['Number of Cases']
    germany_covid_cases['Country/Region'] = 'Germany'

    germany_covid_deaths['Province/State'] = read_file['Federal State']
    germany_covid_deaths[month_day_year] = read_file['Deaths']
    germany_covid_deaths['Country/Region'] = 'Germany'
#     # print(india_covid_deaths)   
#     # print(india_covid)

print(germany_covid_deaths)
cases_file = germany_covid_cases.to_csv(f'/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/aggregated_data/germany_covid_cases.csv')
deaths_file = germany_covid_deaths.to_csv(f'/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/aggregated_data/germany_covid_deaths.csv')