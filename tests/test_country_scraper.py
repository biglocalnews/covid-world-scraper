from unittest.mock import patch, MagicMock

import pytest

from .conftest import file_contents, cache_root
from covid_world_scraper import CountryScraper


class Pak(CountryScraper):

    def fetch(self):
        return ''


def test_run_raises_error_if_missing_required_interfaces():
    with pytest.raises(NotImplementedError) as excep:
        class Bra(CountryScraper):
            pass
        c = Bra()
        c.run()


def test_default_cache_root():
    c = Pak()
    assert str(c.cache_dir).startswith('/tmp/covid-world-scraper')


def test_cache_root_configuration():
    c = Pak('/tmp/foo')
    assert str(c.cache_dir).startswith('/tmp/foo')


def test_scraper_cache_dir():
    "Scraper cache_dir should combine cache root and scraper class name"
    c = Pak()
    assert str(c.cache_dir) == '/tmp/covid-world-scraper/pak'


@pytest.mark.parametrize(
    'attr,expected_val',
    [('raw_dir', 'pak/raw'), ('processed_dir', 'pak/processed')]
)
def test_file_artifact_dirs(attr, expected_val):
    pak = Pak()
    assert str(getattr(pak, attr)).endswith(expected_val)


@pytest.mark.parametrize(
    'hook_name',
    ['pre_process', 'extract', 'post_process']
)
def test_hooks_called_by_run(hook_name):
    "Run should call a series of hooks that can be overridden in subclasses"
    with patch.object(Pak, hook_name) as mock_method:
        pak = Pak()
        pak.run()
        mock_method.assert_called_once()

def test_creation_of_cache_dirs(tmp_path):
    "Run should create cache directories for data files"
    cache_dir = tmp_path.joinpath('covid-world-scraper')
    expected_paths = [
        cache_dir.joinpath('pak/raw'),
        cache_dir.joinpath('pak/processed')
    ]
    pak = Pak(cache_dir)
    pak.run()
    for path in expected_paths:
        assert path.exists()

def test_save_to_raw_cache(cache_root):
    pak = Pak(cache_root)
    contents = "foo bar"
    path = pak.save_to_raw_cache(contents, 'txt')
    assert contents == file_contents(path)
    assert isinstance(path, str)
