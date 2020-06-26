import datetime
from unittest.mock import patch, MagicMock

import pytest

from covid_world_scraper.utils import relative_year


DEC_31 = datetime.datetime(2020, 12, 31, 12, 59, 1)
JAN_1 = datetime.datetime(2020, 1, 1, 1, 1, 1)


@pytest.mark.parametrize(
    'month,day,current_day,expected',
    [
        [12, 31, DEC_31, 2020],
        [12, 31, JAN_1, 2020],
        [1, 1, JAN_1, 2020]
    ]
)
def test_relative_year(month, day, current_day, expected):
    mock_target = 'covid_world_scraper.utils.today'
    with patch(mock_target) as mock_func:
        mock_func.return_value = current_day
        actual = relative_year(month, day)
        assert actual == expected
