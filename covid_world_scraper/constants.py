import pathlib

DEFAULT_CACHE_DIR=str(
    pathlib.Path\
        .home()\
        .joinpath('covid-world-scraper-data')
)
DEFAULT_LOG_FILE=str(pathlib.Path(DEFAULT_CACHE_DIR).joinpath('covid-world-scraper.log'))

