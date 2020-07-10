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
