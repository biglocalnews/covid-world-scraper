import logging
import os
from pathlib import Path

from retrying import retry
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .country_scraper import CountryScraper


logger = logging.getLogger(__name__)


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
        #TODO: Flesh this method out
        logger.info('TODO: Convert {} to a CSV'.format(raw_data_path))
        logger.info('TODO: Store the CSV in {}'.format(self.processed_dir))
        brazil_raw_data = xlrd.open_workbook(raw_data_path)
        sheet = brazil_raw_data.sheet_by_index(0)
        basename = raw_data_path.split('/')[-1].replace('txt','csv')
        outfile_path = str(self.processed_dir.joinpath(basename))
        outfile = open(outfile_path, 'w')
        csv_written = csv.writer(outfile, quoting=csv.QUOTE_ALL)
        for row in range(sheet.nrows):
            csv_written.writerow(sheet.row_values(row))
        outfile.close()
        
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
