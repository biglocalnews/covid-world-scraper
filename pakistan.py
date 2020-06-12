from bs4 import BeautifulSoup
import requests
import pandas as pd

def pakistan():

    # with open('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/HTML/pakistan_covid.htm', 'r') as html:
    #     html_file = html.read()

    #     soup = BeautifulSoup(html_file, 'html.parser')
    #     divs = soup.div

    #     print(divs)

        # div = soup.find("div", class_="table")
        # print(div)


    # url = 'http://covid.gov.pk/stats/pakistan'
    # req = requests.get(url)
    # soup = BeautifulSoup(req.text, 'html.parser')

    # print(soup)
        
    url = 'http://covid.gov.pk/stats/punjab'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    div = soup.find("div", class_="shape ng-scope")
    print(div)

        
        




if __name__ == '__main__':
    pakistan()


