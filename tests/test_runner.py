from unittest.mock import patch, Mock

import pytest

from .conftest import file_contents, cache_root
from covid_world_scraper import (
    CountryScraper,
    Runner,
)

from covid_world_scraper.runner import CountryScraperError


def test_country_codes():
    r = Runner()
    codes = ['BRA', 'PAK']
    assert set(r.country_codes.keys()).issuperset(codes)

def test_country_scrapers_returns_only_counties_default():
    r = Runner()
    names = [s.__name__ for s in r.country_scrapers()]
    assert 'Bra' in names
    assert 'Pak' in names
    assert 'CountryScraper' not in names
    assert 'Runner' not in names

def test_country_scrapers_filter():
    r = Runner()
    names = [s.__name__ for s in r.country_scrapers(filter=['Bra'])]
    assert 'Bra' in names
    assert 'Pak' not in names

def test_country_scrapers_with_incorrect_country_name():
    with pytest.raises(CountryScraperError) as excep:
        r = Runner()
        names = [s.__name__ for s in r.country_scrapers(filter=['Foo'])]

def test_run_is_called_on_country_scrapers():
    # Patch Runner.country_scrapers to return a limited
    # set of countries
    mock_scraper_classes = [
        Mock(name='Bra'),
        Mock(name='Pak'),
    ]
    with patch('covid_world_scraper.runner.Runner.country_scrapers') as mock_method:
        mock_method.return_value = mock_scraper_classes
        r = Runner()
        scrapers = r.run()
        for scraper in scrapers:
            scraper.run.assert_called_once()

def test_list_countries():
    r = Runner()
    countries = r.list_countries()
    assert 'PAK (Pakistan)' in countries
