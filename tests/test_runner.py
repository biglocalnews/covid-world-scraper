from unittest.mock import patch, MagicMock, Mock

import pytest

from .conftest import file_contents, cache_root
from covid_world_scraper import (
    CountryScraper,
    Runner,
)

from covid_world_scraper.alerts import SlackAlertManager
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

def test_send_alerts():
    # Mock two fake scrapers, second of which raises a generic error
    with patch('covid_world_scraper.runner.Runner.country_scrapers') as mock_method:
        mock_scraper_classes = [
            Mock(name='Bra', country_code='BRA'),
            Mock(name='Pak', side_effect=Exception('Woe is me'))
        ]
        mock_method.return_value = mock_scraper_classes
        with patch('covid_world_scraper.alerts.WebClient.chat_postMessage') as mock_post:
            # Configure runner with an alert manager instance
            manager = SlackAlertManager('APIKEY', 'some-channel')
            r = Runner(alert_manager=manager)
            # Run generates messages but does not automatically
            # send them
            r.run()
            mock_post.assert_not_called()
            # Slack client should be called when
            # we request alerts to be sent
            r.send_alerts()
            mock_post.assert_called()
            assert mock_post.call_count == 2
            success_call, error_call = mock_post.call_args_list
            success_msg = success_call[1]['text']
            expected = '1 scraper(s) ran successfully'
            assert expected in success_msg
            error_msg = error_call[1]['text']
            assert 'Woe is me' in error_msg
