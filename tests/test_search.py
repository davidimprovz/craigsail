import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from pathlib import Path
from craigsail.search import Search

@pytest.fixture
def search_instance():
    return Search(search_category='test_category', data_path='test_path', cities=['city1', 'city2'])

def test_get_category(search_instance):
    assert search_instance.get_category() == 'test_category'

def test_set_category(search_instance):
    search_instance.set_category('new_category')
    assert search_instance.get_category() == 'new_category'

def test_add_filters(search_instance):
    search_instance.add_filters(new_filter=True)
    assert 'new_filter' in search_instance.FILTERS

def test_remove_filters(search_instance):
    search_instance.add_filters(new_filter=True)
    search_instance.remove_filters(new_filter=True)
    assert 'new_filter' not in search_instance.FILTERS

def test_add_cities(search_instance):
    search_instance.add_cities(['city3'])
    assert 'city3' in search_instance.CITIES

def test_update_cities(search_instance):
    search_instance.update_cities(['city4'])
    assert 'city4' in search_instance.CITIES
    assert 'city1' not in search_instance.CITIES

def test_remove_cities(search_instance):
    search_instance.remove_cities(['city1'])
    assert 'city1' not in search_instance.CITIES

def test_convert_city_dict_to_df(search_instance):
    city_data = [{'name': 'item1'}, {'name': 'item2'}]
    df = search_instance.convert_city_dict_to_df('city1', city_data)
    assert len(df) == 2
    assert 'city' in df.columns

def test_expand_attributes(search_instance):
    # expand_attributes pivots "key:value" pairs into a one-row frame whose
    # columns are the attribute names - that is the shape expand_all_attributes
    # concatenates onto the listings frame.
    attributes = ['attr1:value1', 'attr2:value2']
    df = search_instance.expand_attributes(attributes)
    assert list(df.columns) == ['attr1', 'attr2']
    assert df['attr1'].iloc[0] == 'value1'


def test_expand_attributes_splits_on_first_colon_only(search_instance):
    df = search_instance.expand_attributes(['engine hours (total):1:30'])
    assert df['engine hours (total)'].iloc[0] == '1:30'

def test_expand_all_attributes(search_instance):
    df = pd.DataFrame({'attrs': [['attr1:value1', 'attr2:value2']]})
    expanded_df = search_instance.expand_all_attributes(df)
    assert 'attr1' in expanded_df.columns
    assert 'attr2' in expanded_df.columns

def test_clean_str_columns(search_instance):
    df = pd.DataFrame({'col1': [' value1 ', ' value2 ']})
    cleaned_df = search_instance.clean_str_columns(df)
    assert cleaned_df['col1'].iloc[0] == 'value1'

def test_strip_nan_columns(search_instance):
    df = pd.DataFrame({'col1': [None, None], 'col2': [1, 2]})
    stripped_df = search_instance.strip_nan_columns(df)
    assert 'col1' not in stripped_df.columns

@patch('craigsail.search.clfs')
def test_get_city_items(mock_clfs, search_instance):
    mock_clfs.return_value.get_results.return_value = [{'name': 'item1'}, {'name': 'item2'}]
    city_df = search_instance.get_city_items('city1')
    assert len(city_df) == 2

@patch('craigsail.search.pd.to_datetime')
def test_get_all_daily_postings(mock_to_datetime, search_instance):
    mock_to_datetime.side_effect = [pd.Timestamp('2023-01-01'), pd.Timestamp('2023-01-02')]
    with patch.object(search_instance, 'get_city_items', return_value=pd.DataFrame({'name': ['item1']})):
        timespan, df = search_instance.get_all_daily_postings()
        assert timespan.days == 1
        # one row per city in the fixture (city1, city2)
        assert len(df) == 2

def test_save_data_as_csv(tmp_path):
    # Use a real temp dir: save_data_as_csv creates the directory, so mocking
    # to_csv alone would leave a stray folder in the repo.
    search = Search(search_category='test_category', data_path=str(tmp_path), cities=['city1'])
    df = pd.DataFrame({'name': ['item1']})

    save_path = search.save_data_as_csv(df, 'test_file')

    assert save_path.exists()
    assert pd.read_csv(save_path)['name'].iloc[0] == 'item1'

@patch('craigsail.search.pd.DataFrame.to_sql')
def test_send_to_sqlitedb(mock_to_sql, search_instance):
    df = pd.DataFrame({'name': ['item1']})
    conn = MagicMock()
    search_instance.send_to_sqlitedb(df, conn, 'test_table')
    mock_to_sql.assert_called_once()

def test_filter_feature_space(search_instance):
    df = pd.DataFrame({'col1': [1], 'col2': [2]})
    filtered_df = search_instance.filter_feature_space(df, ['col1'])
    assert 'col1' in filtered_df.columns
    assert 'col2' not in filtered_df.columns

def test_merge_multiple_csvs(search_instance, tmp_path):
    # Write real CSVs: mocking read_csv left the glob empty, so the function
    # under test never actually merged anything.
    pd.DataFrame({'merge_col': [1, 2], 'price_day1': [10, 20]}).to_csv(tmp_path / 'day1.csv', index=False)
    pd.DataFrame({'merge_col': [1, 2], 'price_day2': [11, 19]}).to_csv(tmp_path / 'day2.csv', index=False)

    merged_df = search_instance.merge_multiple_csvs(str(tmp_path), 'merge_col')

    assert 'merge_col' in merged_df.columns
    assert 'price_day1' in merged_df.columns
    assert 'price_day2' in merged_df.columns
    assert len(merged_df) == 2
