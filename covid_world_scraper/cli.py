import importlib
import logging

import click


@click.command(
    help="3-letter country codes for one or more countries. Multiple abbreviations can be "
)
@click.argument('countries', nargs=-1)
@click.option('--all', is_flag=True, help="Scrape all countries")
def cli(countries, all):
    """Scrape data for one or more countries."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)-12s - %(message)s',
        datefmt='%m-%d %H:%M',
        filename='/tmp/covid-world-scraper.log',
        filemode='a'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    if all:
        click.echo("Scraping all countries")
    else:
        for country in countries:
            mod_name = country.strip().lower()
            kls_name = mod_name.title()
            try:
                mod = importlib.import_module('covid_world_scraper.{}'.format(mod_name))
                ScraperKls = getattr(mod, kls_name)
            except (ModuleNotFoundError, ImportError, AttributeError):
                click.echo("Unable to find scraper {}".format(kls_name))
                return 1
            ScraperKls().run()
