import logging
import shutil
import tempfile
import time
from pathlib import Path

from retrying import retry
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .country_scraper import CountryScraper
from .errors import DownloadInProgressError

import pandas as pd

logger = logging.getLogger(__name__)


class Bra(CountryScraper):

    temp_dir = Path(tempfile.gettempdir()).joinpath('covid-world-scraper')

    def pre_process(self):
        # Remove any old non-standard and/or partial files
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        previous = self.temp_dir.glob("*PAINEL_COVID*")
        for p in previous:
            p.unlink()

    def fetch(self):
        url = 'https://covid.saude.gov.br/'
        opts = Options()
        opts.headless = self.headless_status
        driver = webdriver.Firefox(
            firefox_profile=self.ff_profile(str(self.temp_dir)),
            options=opts
        )
        try:
            driver.get(url)
            time.sleep(10)
            date = driver.find_elements_by_xpath('/html/body/app-root/ion-app/ion-router-outlet/app-home/ion-content/div[1]/div[1]/div[3]/span')[0].get_attribute('innerText')
            buttons = driver.find_elements_by_tag_name('ion-button')
            for button in buttons:
                if button.text.lower().strip() == 'arquivo csv':
                    button.click()
                    target_file = self._get_file_name(self.temp_dir)
                    logger.info('Downloaded {}'.format(target_file))
                    standardized_name = self._rename_xlxs(target_file)
                    logger.info('Renamed file to {}'.format(standardized_name))
                    final_outfile = self._transfer_temp_file_to_raw_dir(standardized_name)
                    logger.info('Copied {} to {}'.format(standardized_name, final_outfile))
                    return {
                        'cached_text_path': final_outfile,
                        'temp_source_file': standardized_name,
                        'date': date,
                    }
        finally:
            driver.quit()

    def extract(self, payload):
        raw_data_path = payload['temp_source_file']
        date = payload['date']

        # start to pandas solution
        basename = raw_data_path.split('/')[-1].replace('xlsx', 'csv')
        outfile_path = str(self.processed_dir.joinpath(basename))

        df = pd.read_excel(raw_data_path, sheet_name=None)
        df['Sheet 1']['date'] = date
        df['Sheet 1']['scrape_date'] = self.runtimestamp
        df['Sheet 1'].to_csv(outfile_path)
        logger.info("Created {}".format(outfile_path))

        return outfile_path

    def post_process(self):
        # Clobber all tempfiles from this or earlier runs
        previous = self.temp_dir.glob("*.xlsx")
        for p in previous:
            p.unlink()

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

        *_PAINEL_COVIDBR_21jun2020.xlsx
        *_PAINEL_COVIDBR_21jun2020.xlsx.part
        """
        target_files = list(download_dir.glob("*PAINEL_COVIDBR*"))
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

    def _transfer_temp_file_to_raw_dir(self, source_path):
        # File transfer is necessary to work around lack of support
        # for mv operations on a gcsfuse-mounted Google Cloud Storage
        # bucket.
        source = Path(source_path)
        dest = str(self.raw_dir.joinpath(source.name))
        shutil.copy(str(source_path), dest)
        return dest
