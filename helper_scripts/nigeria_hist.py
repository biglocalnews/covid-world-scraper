from selenium import webdriver
from selenium.webdriver.common.by import By

def nigeria_hist():

    # chrome_options = webdriver.ChromeOptions()
    # prefs = {'download.default_directory' : '/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/pdfs'}
    # chrome_options.add_experimental_option('prefs', prefs)
    # driver = webdriver.Chrome('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/chromedriver', chrome_options=chrome_options)

    # clicks element but no download

    # options = webdriver.ChromeOptions()
    # options.add_argument("--start-maximized")
    # prefs = {"profile.default_content_settings.popups": 0,
    #             "download.default_directory": 
    #                         "/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/pdfs",
    #             "directory_upgrade": True}
    # options.add_experimental_option("prefs", prefs)
    # driver=webdriver.Chrome('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/chromedriver', options=options)

    # clicks element but no download

    driver = webdriver.Chrome('/Users/dilcia_mercedes/Big_Local_News/prog/pitch_intl/PITCH/chromedriver') 
    driver.get('https://ncdc.gov.ng/diseases/sitreps/?cat=14&name=An%20update%20of%20COVID-19%20outbreak%20in%20Nigeria')
    elem = driver.find_element(By.XPATH, "/html/body/div[2]/section/div[3]/table/tbody/tr[1]/td[4]/a")
    elem.click()
    print('element clicked')
    


if __name__ == '__main__':
    nigeria_hist()