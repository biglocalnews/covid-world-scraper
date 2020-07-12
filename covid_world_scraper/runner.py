import importlib
import logging
import pkgutil

import covid_world_scraper
from .constants import DEFAULT_CACHE_DIR
from .country_codes import COUNTRY_CODES

from .alerts import SlackAlertManager

logger = logging.getLogger(__name__)

class CountryScraperError(Exception): pass


class Runner:
    """
    Facade class to simplify invocation
    and usage of country scrapers by the
    cli module.
    """

    country_codes = COUNTRY_CODES

    def __init__(self, alert_manager=None):
        self.alert_manager = alert_manager

    def run(self, cache_dir=DEFAULT_CACHE_DIR, headless_status=True, filter=[]):
        """
        Run country scrapers.

        Keyword arguments:
        cache_dir -- Path to cache directory for scraped file artifacts (default: {})
        headless_status -- Whether or not to run headless (default: True)
        filter -- List of 3-letter country codes that limits countries to be scraped.

        Returns: List of CountryScrapers
        """.format(DEFAULT_CACHE_DIR)
        scraper_objs = []
        for ScraperKls in self.country_scrapers(filter=filter):
            try:
                scraper = ScraperKls(cache_dir, headless_status=headless_status)
                scraper.run()
                scraper_objs.append(scraper)
            except Exception as e:
                message = str(e)
                level = 'ERROR'
                if self.alert_manager:
                    self.alert_manager.add(message, level)
                logger.error(message)
        # Add generic alert message listing countries
        # scraped successfully
        success_msg = self._prep_success_message(scraper_objs)
        if self.alert_manager:
            self.alert_manager.insert(0, success_msg, 'INFO')
        logger.info(success_msg)
        return scraper_objs

    def _prep_success_message(self, scraper_objs):
        count = len(scraper_objs)
        if count > 0:
            names = ', '.join([
                str(s.country_code) for s in scraper_objs
            ])
            message = "{} scraper(s) ran successfully: {}".format(count, names)
        else:
            message = "Zero scrapers ran successfully"
        return message

    def send_alerts(self):
        self.alert_manager.send()

    def list_countries(self):
        """
        List available country scrapers.

        Returns: List of country codes and names.
        """
        return [str(ScraperKls()) for ScraperKls in self.country_scrapers()]

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
