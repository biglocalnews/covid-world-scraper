import datetime
import os
import pandas as pd
from pitch_last7 import get_last_seven

## UPDATE THIS WITH `GET HSITORICAL DATA` SCRIPT

date = datetime.datetime.now()
year = date.year
day = date.day
month = date.month
month = str(month).zfill(2)
day = str(day).zfill(2)
print(year, day, month)

date_input = f'{month}_{day}'

hi = get_last_seven(date_input)
# print(hi)

path = '/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/old_data'

headers = ['Province/State', 'Country/Region']
india_covid_cases = pd.DataFrame(columns = headers)
india_covid_deaths = pd.DataFrame(columns = headers)

# month_day_year = f'{month}/{day}/{year}'

for file in hi:

    full_file = f'{path}/{file}_india_covid19.csv'

    file = file.split('-')
    month_day_year = f'{file[1]}/{file[2]}/{file[0]}'
    read_file = pd.read_csv(full_file)
    read_file = read_file.iloc[: -2, :] # dropping totals column

    # print(read_file.columns)

    india_covid_cases['Province/State'] = read_file['Name of State / UT']
    india_covid_cases[month_day_year] = read_file['Total Confirmed cases*']
    india_covid_cases['Country/Region'] = 'India'

    india_covid_deaths['Province/State'] = read_file['Name of State / UT']
    india_covid_deaths[month_day_year] = read_file['Deaths**']
    india_covid_deaths['Country/Region'] = 'India'
    # print(india_covid_deaths)   
    # print(india_covid)

print(india_covid_cases)
    # 





    # what to do about cases being re-assigned to states?