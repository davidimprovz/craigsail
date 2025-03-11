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
    attributes = ['attr1:value1', 'attr2:value2']
    df = search_instance.expand_attributes(attributes)
    assert 'Attributes' in df.columns
    assert 'Values' in df.columns

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
        assert len(df) == 1

@patch('craigsail.search.pd.DataFrame.to_csv')
def test_save_data_as_csv(mock_to_csv, search_instance):
    df = pd.DataFrame({'name': ['item1']})
    search_instance.save_data_as_csv(df, 'test_file')
    mock_to_csv.assert_called_once()

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

@patch('craigsail.search.pd.read_csv')
def test_merge_multiple_csvs(mock_read_csv, search_instance):
    mock_read_csv.return_value = pd.DataFrame({'merge_col': [1], 'col1': [2]})
    merged_df = search_instance.merge_multiple_csvs('test_path', 'merge_col')
    assert 'merge_col' in merged_df.columns
