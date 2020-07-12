import logging
from unittest.mock import patch, DEFAULT

import pytest
from pathlib import Path
from click.testing import CliRunner

from .conftest import cache_root
from covid_world_scraper.cli import cli

def test_list_countries():
    runner = CliRunner()
    result = runner.invoke(cli, ['--list-scrapers'])
    assert result.exit_code == 0
    assert '- BRA (Brazil)' in result.output
    assert '- PAK (Pakistan)' in result.output

def test_cache_dir_creation(cache_root):
    cache_dir = Path(cache_root).joinpath('covid-world-scraper-data')
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            '--cache-dir={}'.format(str(cache_dir)),
            '--list-scrapers'
        ]
    )
    assert cache_dir.exists

def test_slack_alert_config_error(caplog):
    caplog.set_level(logging.INFO)
    with patch('covid_world_scraper.cli.Runner.run') as mock_method:
        runner = CliRunner()
        runner.invoke(cli, ['--alert','--all'])
        expected = "WARNING - Slack alerts will not be sent.\n" + \
                "Please ensure you've configured the below environment variables:\n" + \
                "COVID_WORLD_SLACK_API_KEY=YOUR_API_KEY\n" + \
                "COVID_WORLD_SLACK_CHANNEL=channel-name"
        assert expected in caplog.text

def test_slack_alert_configured_correctly(caplog, monkeypatch):
    monkeypatch.setenv(
        'COVID_WORLD_SLACK_API_KEY',
        'AN_API_KEY'
    )
    monkeypatch.setenv(
        'COVID_WORLD_SLACK_CHANNEL',
        'some-channel'
    )
    caplog.set_level(logging.INFO)
    with patch('covid_world_scraper.cli.Runner.run') as mock_method:
        runner = CliRunner()
        runner.invoke(cli, ['--alert','--all'])
        expected = "Slack alerts will be sent to #some-channel."
        assert expected in caplog.text

def test_runner_sends_alerts(monkeypatch):
    monkeypatch.setenv(
        'COVID_WORLD_SLACK_API_KEY',
        'AN_API_KEY'
    )
    monkeypatch.setenv(
        'COVID_WORLD_SLACK_CHANNEL',
        'some-channel'
    )
    with patch('covid_world_scraper.cli.Runner.run') as mock_run:
        with patch('covid_world_scraper.cli.Runner.send_alerts') as mock_send:
            runner = CliRunner()
            runner.invoke(cli, ['--alert','--all'])
            mock_run.assert_called_once()
            mock_send.assert_called_once()

def test_runner_does_not_alert_by_default(monkeypatch):
    monkeypatch.setenv(
        'COVID_WORLD_SLACK_API_KEY',
        'AN_API_KEY'
    )
    monkeypatch.setenv(
        'COVID_WORLD_SLACK_CHANNEL',
        'some-channel'
    )
    with patch('covid_world_scraper.cli.Runner.run') as mock_run:
        with patch('covid_world_scraper.cli.Runner.send_alerts') as mock_send:
            runner = CliRunner()
            runner.invoke(cli, ['--all'])
            mock_run.assert_called_once()
            mock_send.assert_not_called()

def test_scrapers_run_if_alert_misconfigured():
    "Scrapers should run even if alerts are requested but misconfigured"
    with patch('covid_world_scraper.cli.Runner.run') as mock_run:
        with patch('covid_world_scraper.cli.Runner.send_alerts') as mock_send:
            runner = CliRunner()
            runner.invoke(cli, ['--alert', '--all'])
            mock_run.assert_called_once()
            mock_send.assert_not_called()
