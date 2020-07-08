import importlib
import logging
import pathlib
import pkgutil

import click

import covid_world_scraper
from .country_codes import COUNTRY_CODES

DEFAULT_CACHE_DIR=str(
    pathlib.Path\
        .home()\
        .joinpath('covid-world-scraper-data')
)
DEFAULT_LOG_FILE=str(pathlib.Path(DEFAULT_CACHE_DIR).joinpath('covid-world-scraper.log'))

@click.command(
    help="3-letter country codes for one or more countries. Multiple abbreviations can be "
)
@click.argument('countries', nargs=-1)
@click.option('--all', is_flag=True, help="Scrape all available countries")
@click.option(
    '--cache-dir',
    default=DEFAULT_CACHE_DIR,
    show_default=DEFAULT_CACHE_DIR,
    help="Location to store scraped data files."
)
@click.option(
    '--log-file',
    default=DEFAULT_LOG_FILE,
    show_default=DEFAULT_LOG_FILE,
    help="Scraper log file location."
)
@click.option(
    '--headless/--with-browser',
    default=True,
    show_default="--headless",
    help="Enable/disable headless mode for Selenium-based browsers."
)
def cli(countries, all, cache_dir, log_file, headless):
    """Scrape data for one or more countries."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)-12s - %(message)s',
        datefmt='%m-%d %H:%M',
        filename=log_file,
        filemode='a'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    if all:
        all_codes = set(COUNTRY_CODES.keys())
        # modname should be 3-letter ISO code used in country scraper modules, e.g. pak.py
        for importer, modname, ispkg in pkgutil.iter_modules(covid_world_scraper.__path__):
            if modname.upper() in all_codes:
                try:
                    ScraperKls = get_scraper_class(modname)
                except AttributeError:
                    # country scrapers that don't contain a properly named class
                    # are silently skipped.
                    pass
                ScraperKls(cache_dir, headless_status=headless).run()
    else:
        for country in countries:
            try:
                ScraperKls = get_scraper_class(country)
            except (ModuleNotFoundError, ImportError, AttributeError):
                click.echo("Unable to find scraper {}".format(kls_name))
                return 1
            ScraperKls(cache_dir, headless_status=headless).run()

def get_scraper_class(country):
    mod_name = country.replace('.py','').strip().lower()
    kls_name = mod_name.title()
    mod = importlib.import_module('covid_world_scraper.{}'.format(mod_name))
    return getattr(mod, kls_name)
