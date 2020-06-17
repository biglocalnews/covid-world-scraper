"""
Official page for Pakistan COVID figures:

    http://covid.gov.pk/stats/pakistan

The above page contains an iframe with the target data.
This scraper hits the iframe page directly.

We'll need to test if the iframe URL on the home page changes over time,
If so, we'll need to first scrape the home page for the latest
iframe URL, then grab the data from the source page on the datastudio.google.com.

"""
import csv
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def main():
    data = scrape()
    write_csv(data)

def scrape():
    url = "https://datastudio.google.com/embed/reporting/1PLVi5amcc_R5Gh928gTE8-8r8-fLXJQF/page/R24IB"
    opts = Options()
    opts.headless = True
    data = []
    try:
        driver = webdriver.Firefox(options=opts)
        driver.get(url)
        # Gross, but works
        time.sleep(20)
        tables = driver.find_elements_by_css_selector('lego-table.table.ng-scope')
        for tbl in tables:
            text = tbl.text.strip().replace(',','')
            if text.startswith('AJK'):
                data = chunks(text.split('\n'))
    finally:
        driver.quit()
    return data

def chunks(lst):
    chunk_size = 5
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def write_csv(data):
    header = [
        'admin_unit',
        'confirmed_cases',
        'active_cases',
        'deaths',
        'recoveries'
    ]
    outfile = 'covid_cases_pakistan.csv'
    with open(outfile,'w') as out:
        writer = csv.writer(out)
        writer.writerow(header)
        writer.writerows(data)
    print("File written: {}".format(outfile))

if __name__ == '__main__':
    main()
