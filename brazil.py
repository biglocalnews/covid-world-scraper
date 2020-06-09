from bs4 import BeautifulSoup
import requests
import pandas as pd

def brazil():

    with open('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/HTML/brazil_covid.htm', 'r') as html:
        html_file = html.read()

        soup = BeautifulSoup(html_file, 'html.parser')
        # no table apparently




if __name__ == '__main__':
    brazil()