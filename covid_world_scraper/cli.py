import logging
from pathlib import Path

import click

from covid_world_scraper import Runner
from covid_world_scraper.constants import (
    DEFAULT_CACHE_DIR,
    DEFAULT_LOG_FILE,
)



@click.command(
    help="3-letter country codes for one or more countries. Multiple abbreviations can be "
)
@click.argument('countries', nargs=-1)
@click.option(
    '-a',
    '--all',
    is_flag=True,
    help="Scrape all available countries"
)
@click.option(
    '--cache-dir',
    default=DEFAULT_CACHE_DIR,
    show_default=DEFAULT_CACHE_DIR,
    help="Location to store scraped data files."
)
@click.option(
    '-l',
    '--list-scrapers',
    is_flag=True,
    help="List countries available to scrape."
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
def cli(countries, all, cache_dir, list_scrapers, log_file, headless):
    """Scrape data for one or more countries."""
    # Ensure cache directory exists
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
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
    runner = Runner()
    if list_scrapers:
        click.echo('Available country scrapers:')
        for country in runner.list_countries():
            msg = '- {}'.format(country)
            click.echo(msg)
    else:
        kwargs = {
            'cache_dir': cache_dir,
            'headless_status': headless,
            'filter': countries,
        }
        runner.run(**kwargs)
