import csv
import logging
import os
import xlrd
from pathlib import Path

from retrying import retry
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .country_scraper import CountryScraper

from datetime import date,datetime,time
from xlrd import open_workbook,xldate_as_tuple
from xlrd import open_workbook,cellname

logger = logging.getLogger(__name__)

# renamed from bra to old_bra


class DownloadInProgressError(Exception):
    pass


class Bra(CountryScraper):

    def pre_process(self):
        # Remove any old non-standard and/or partial files
        previous = self.raw_dir.glob("HIST*")
        for p in previous:
            p.unlink()

    def fetch(self):
        url = 'https://covid.saude.gov.br/'
        opts = Options()
        opts.headless = True
        data = []
        driver = webdriver.Firefox(
            firefox_profile=self.ff_profile(str(self.raw_dir)),
            options=opts
        )
        try:
            driver.get(url)
            buttons = driver.find_elements_by_tag_name('ion-button')
            for button in buttons:
                if button.text.lower().strip() == 'arquivo csv':
                    button.click()
                    target_file = self._get_file_name(self.raw_dir)
                    logger.info('Downloaded {}'.format(target_file))
                    standardized_name = self._rename_xlxs(target_file)
                    logger.info('Renamed file to {}'.format(standardized_name))
                    return standardized_name
        finally:
            driver.quit()

    def extract(self, raw_data_path):
        logger.info('Extracting data from {}'.format(raw_data_path))
        brazil_raw_data = xlrd.open_workbook(raw_data_path)


        sheet = brazil_raw_data.sheet_by_index(0)

        # print("{0} {1} {2}".format(sheet.name, sheet.nrows, sheet.ncols))

        # for rx in range(sheet.ncols):
        #     print(sheet.col(rx))
        # These lines above did not work - these are straight out of the Quickstart sections of the README on github
        # https://github.com/python-excel/xlrd

        
        # print(sheet.nrows)
        # print(sheet.ncols)
        # The above lines gave me errors

        # for row_index in range(sheet.nrows):
        #     for col_index in range(sheet.ncols):
        #         print(cellname(row_index,col_index), '-')
        #         print(sheet.cell(row_index, col_index).value)


        # date_value = xldate_as_tuple(sheet.cell(2,7).value,brazil_raw_data.datemode) 
        # this is one of the cells w/ a date
        # print(date_value, ' date value')
        # print(datetime(*date_value), date(*date_value[:3]))
        # Got these lines of code from some xlrd docs https://github.com/python-excel/tutorial (click link at the bottom of page for full docs - go to page 13 to understand how to convert date information)

        basename = raw_data_path.split('/')[-1].replace('xlsx','csv')
        outfile_path = str(self.processed_dir.joinpath(basename))
        outfile = open(outfile_path, 'w')
        csv_written = csv.writer(outfile)
        for row in range(sheet.nrows):
            csv_written.writerow(sheet.row_values(row))
        outfile.close()
        logger.info('Created {}'.format(outfile_path))
        return outfile_path
        
    def ff_profile(self, download_dir):
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

    @retry(
        stop_max_attempt_number=7,
        stop_max_delay=30000,
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000
    )
    def _get_file_name(self, download_dir):
        """
        The file names below are examples of the raw data naming convention. 

        HIST_PAINEL_COVIDBR_21jun2020.xlsx
        HIST_PAINEL_COVIDBR_21jun2020.xlsx.part
        """
        target_files = list(download_dir.glob("HIST_PAINEL_COVIDBR*"))
        if len(target_files) == 1 and str(target_files[0]).endswith('.xlsx'):
            logger.info("Download complete")
            return str(target_files[0])
        if len(target_files) > 1:
            logger.info("Download not yet complete...")
            raise DownloadInProgressError
        else:
            raise Exception("Unexpected downloading condition encountered.")

    def _rename_xlxs(self, full_path):
        original = Path(full_path)
        new_name = original.parent.joinpath("{}.xlsx".format(self.runtimestamp))
        original.rename(new_name)
        return str(new_name)
