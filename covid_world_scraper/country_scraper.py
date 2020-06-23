import csv
import logging

from pathlib import Path
from datetime import datetime


logger = logging.getLogger(__name__)


class CountryScraper:
    """Base class for country-specific scrapers.

    Scraper subclasses should use 3-letter ISO country code
    for their class and module names.

    All subclasses must implement the "fetch" method.

    USAGE:
        # pak.py

        from .country_scraper import CountryScraper
        class Pak(CountryScraper)

            def fetch(self):
                # do a bunch o' web scraping here
                pass
    """

    def __init__(self, cache_dir='/tmp/covid-world-scraper'):
        self.runtime = self._set_runtime()
        self.cache_dir = Path(
            cache_dir,
            self._klass_name.lower()
        )
        self.raw_dir = self.cache_dir.joinpath('raw')
        self.processed_dir = self.cache_dir.joinpath('processed')

    def run(self):
        logger.info("START SCRAPE - {}".format(self._klass_name))
        self._create_cache_dirs()
        self.pre_process()
        raw_data_path = self.fetch()
        self.extract(raw_data_path)
        self.post_process()
        logger.info("END SCRAPE - {}".format(self._klass_name))

    def fetch(self):
        """Downloads source file(s) to local cache.

        Files should be saved to the "raw" directory inside
        the country's cache directory. Files should be named
        using a UTC timestamp and file extension:

            YYYYMMDDTHHMMZ.ext

        Examples:

            /tmp/covid-scraper/pak/raw/20200301T0101Z.html
            /tmp/covid-scraper/bra/raw/20200301T0101Z.xlsx

        RETURNS

            Path to downloaded file
        """
        raise NotImplementedError

    def extract(self, raw_data_path):
        """Perform data extraction from raw source data,
        if necessary, and generate an alternative format,
        (typically CSV) with high fidelity to the raw data.

        Extracted data should be saved to the country's
        "processed" directory using the following naming convention:

            YYYYMMDDTHHMMZ.ext

        The name of the processed file should match the source file in
        the "raw" directory, but should have a new file extension.

        Examples:

            /tmp/covid-scraper/pak/processed/20200301T0101Z.csv
            /tmp/covid-scraper/bra/processed/20200301T0101Z.json


        RETURNS

            Path to processed file
        """
        pass

    def pre_process(self):
        """Perform preliminary setup or processing, if
        necessary, prior to fetching data.
        """
        pass

    def post_process(self, *args, **kwargs):
        """Perform teardown or final processing, if
        necessary, after fetching data.
        """
        pass

    def save_to_raw_cache(self, content, extension):
        basename = "{}.{}".format(self.runtimestamp, extension)
        outfile = self.raw_dir.joinpath(basename)
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        with open(outfile, 'w') as out:
            out.write(content)
        logger.info("Saved {}".format(outfile))
        return str(outfile)

    def processed_filepath_from_raw(self, raw_path, new_extension):
        return raw_path\
                .replace('raw', 'processed')\
                .split('.')[0] +\
                '.{}'.format(new_extension)

    def write_csv(self, data, outfile, headers=[]):
        with open(outfile,'w') as out:
            writer = csv.writer(out)
            if headers:
                writer.writerow(headers)
            writer.writerows(data)
        logger.info("Saved extracted data to {}".format(outfile))

    def _set_runtime(self):
        return datetime.utcnow()

    @property
    def runtimestamp(self):
        return self.runtime.strftime("%Y%m%dT%H%MZ")

    @property
    def _klass_name(self):
        return self.__class__.__name__

    def _create_cache_dirs(self):
        kwargs = {
            'parents': True,
            'exist_ok': True
        }
        self.raw_dir.mkdir(**kwargs)
        self.processed_dir.mkdir(**kwargs)

    @property
    def _screenshot_path(self):
        basename = "{}.png".format(self.runtimestamp)
        outfile = self.raw_dir.joinpath(basename)
        return str(outfile)
