import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from pathlib import Path
from craigsail.search import Boats

@pytest.fixture
def boats_instance():
    return Boats(search_category='boo', data_path='test_path', cities=['city1'])

def test_combine_city_sailboats_data(boats_instance):
    df = pd.DataFrame({'mfg_year': [None, 2000], 'año de fabricación': [1999, None]})
    combined_df = boats_instance.combine_city_sailboats_data(df)
    assert 'year manufactured' in combined_df.columns

def test_clean_city_sailboats_data(boats_instance):
    df = pd.DataFrame({'name': ['Boat 1999'], 'price': ['$1,000']})
    cleaned_df = boats_instance.clean_city_sailboats_data(df)
    assert cleaned_df['price'].iloc[0] == 1000.0
