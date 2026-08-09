from unittest.mock import patch

import pandas as pd
import pytest

from craigsail.cli import CATEGORY_CLASSES, main, parse_filters
from craigsail.db import CraigsailDB
from craigsail.search import Boats, Search


def test_parse_filters_coerces_types():
    filters = parse_filters(['max_price=5000', 'search_titles=true', 'query=sailboat'])
    assert filters == {'max_price': 5000, 'search_titles': True, 'query': 'sailboat'}


def test_parse_filters_rejects_bare_values():
    with pytest.raises(ValueError):
        parse_filters(['max_price'])


def test_category_maps_to_subclass():
    assert CATEGORY_CLASSES['boo'] is Boats
    assert CATEGORY_CLASSES.get('unknown', Search) is Search


def test_bad_city_exits_without_traceback(tmp_path, capsys):
    with patch.object(Search, 'validate_cities', side_effect=ValueError('Unknown craigslist site(s)')):
        code = main(['--search_category', 'boo', '--data_path', str(tmp_path), '--cities', 'nope'])

    assert code == 2
    assert 'Unknown craigslist site' in capsys.readouterr().err


def test_main_persists_results_to_db(tmp_path):
    postings = pd.DataFrame([{
        'id': '99', 'name': 'Test boat', 'url': 'http://x/99', 'city': 'sfbay',
        'price': '$3,000', 'where': 'marina', 'geotag': (37.8, -122.4), 'has_image': True,
    }])

    with patch.object(Search, 'validate_cities', return_value=['sfbay']), \
         patch.object(Boats, 'get_all_daily_postings',
                      return_value=(pd.Timedelta(seconds=5), postings)):
        code = main(['--search_category', 'boo', '--data_path', str(tmp_path), '--cities', 'sfbay'])

    assert code == 0

    saved = CraigsailDB(str(tmp_path / 'craigsail.db')).load_listings()
    assert len(saved) == 1
    assert saved['price'].iloc[0] == 3000.0


def test_main_csv_flag_writes_snapshot(tmp_path):
    postings = pd.DataFrame([{'id': '1', 'name': 'Boat', 'price': '$10', 'city': 'sfbay'}])

    with patch.object(Search, 'validate_cities', return_value=['sfbay']), \
         patch.object(Boats, 'get_all_daily_postings',
                      return_value=(pd.Timedelta(seconds=1), postings)):
        main(['--search_category', 'boo', '--data_path', str(tmp_path), '--cities', 'sfbay', '--csv'])

    assert list(tmp_path.glob('search_results_*.csv'))
