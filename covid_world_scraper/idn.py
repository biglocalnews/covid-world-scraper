import os
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def indonesia():

    # switched to selenium

    url = 'https://covid19.kemkes.go.id/category/situasi-infeksi-emerging/info-corona-virus/#.XuvC8GpKjRb'
    opts = Options()
    opts.headless = True
    data = []
    try:
        driver = webdriver.Firefox(
            firefox_profile=ff_profile(),
            options=opts
        )
        driver.get(url)

        first_link = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/article[1]/h2/a").click()
        # how do I make sure the right thing is being clicked?
        # what are the advantages of running headless?

    finally:
        driver.quit()



def ff_profile(download_dir=os.getcwd()):
    # Configure Firefox profile to avoid triggering pop-up
    # that requests permission to download, per Selenium docs:
    # https://selenium-python.readthedocs.io/faq.html#how-to-auto-save-files-using-custom-firefox-profile
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", download_dir)
    fp.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    return fp


    # BeautifulSoup based scraper
    # page = requests.get(url)
    # soup = BeautifulSoup(page.text, 'html.parser')

    # data_link = soup.find_all("a")[51]
    # link = data_link.get("href")
    
    # page_2 = requests.get(link)
    # soup_2 = BeautifulSoup(page_2.text, 'html.parser')
    # pdf_link = soup_2.find_all("a")[52]
    # link2 = data_link.get("href")

    # page_3 = requests.get(pdf_link, stream=True)
    # file_name = f'{today_date}_indonesia_covid19.pdf'
    # base_path = os.environ['TO_PDF_DIR']
    # full_path = f'{base_path}/{file_name}'

    # with open(full_path, 'wb') as cov_pdf:
    #     for chunk in page_3.iter_content(chunk_size=128):
    #         cov_pdf.write(chunk)

    # counter = 0
    # for link in pdf_link:
    #     print(link)
    #     print(counter)
    #     counter += 1



    


if __name__ == '__main__':
    indonesia()