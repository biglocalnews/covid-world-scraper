import importlib
import logging
import pkgutil

import covid_world_scraper
from .constants import DEFAULT_CACHE_DIR
from .country_codes import COUNTRY_CODES


logger = logging.getLogger(__name__)

class CountryScraperError(Exception): pass


class Runner:
    """
    Facade class to simplify invocation
    and usage of country scrapers by the
    cli module.
    """

    country_codes = COUNTRY_CODES

    def run(self, cache_dir=DEFAULT_CACHE_DIR, headless_status=True, filter=[]):
        """
        Run country scrapers.

        Keyword arguments:
        cache_dir -- Path to cache directory for scraped file artifacts (default: {})
        headless_status -- Whether or not to run headless (default: True)
        filter -- List of 3-letter country codes that limits countries to be scraped.

        Returns: None
        """.format(DEFAULT_CACHE_DIR)
        scraper_objs = []
        for ScraperKls in self.country_scrapers(filter=filter):
            scraper = ScraperKls(cache_dir, headless_status=headless_status)
            scraper.run()
            scraper_objs.append(scraper)
        return scraper_objs

    def country_scrapers(self, filter=[]):
        """
        Return scraper classes for all available countries.

        Keyword arguments:
        filter -- list of 3-letter country codes that limits return value

        Returns: List of CountryScraper subclasses
        """
        scrapers = []
        if filter:
            for country in filter:
                try:
                    scrapers.append(self._get_scraper_class(country))
                except (ModuleNotFoundError, ImportError, AttributeError):
                    msg = "Unable to find scraper for {}".format(country)
                    logger.error(msg)
                    raise CountryScraperError(msg)
        else:
            for importer, modname, ispkg in pkgutil.iter_modules(covid_world_scraper.__path__):
                if modname.upper() in self.country_codes.keys():
                    try:
                        scrapers.append(self._get_scraper_class(modname))
                    except AttributeError:
                        # country scrapers that don't contain a properly named class
                        # are silently skipped.
                        pass
        return scrapers

    def _get_scraper_class(self, country):
        mod_name = country.replace('.py','').strip().lower()
        kls_name = mod_name.title()
        mod = importlib.import_module('covid_world_scraper.{}'.format(mod_name))
        return getattr(mod, kls_name)
