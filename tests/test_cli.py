from click.testing import CliRunner


from covid_world_scraper.cli import cli

def test_list_countries():
    runner = CliRunner()
    result = runner.invoke(cli, ['--list-scrapers'])
    assert result.exit_code == 0
    assert '- BRA (Brazil)' in result.output
    assert '- PAK (Pakistan)' in result.output

#TODO
def test_cache_dir_creation():
    pass
