import pytest


@pytest.fixture
def cache_root(tmp_path):
    return str(tmp_path.joinpath('covid-world-scraper'))

def file_contents(pth):
    with open(pth, 'r') as f:
        return f.read()
