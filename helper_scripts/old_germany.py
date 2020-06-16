#!/usr/bin/python
import requests as req
from pathlib import Path
import os
import shutil
from datetime import date

def move_data_ger():

    today_date = date.today()
    start_path = '/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/Data/'
    end_path = '/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/old_data/'

    dirs = os.listdir(start_path)
    for file in dirs:
        if 'south_africa' in file:
            full_start_path = f'{start_path}{file}'
            full_end_path = f'{end_path}{file}'
        else:

            full_start_path = f'{start_path}{file}'
            full_end_path = f'{end_path}{today_date}_{file}'
            print(full_start_path)
        shutil.move(full_start_path, full_end_path)

if __name__ == '__main__':
    move_data_ger()