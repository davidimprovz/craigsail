import pandas as pd
import pytest

from craigsail.db import CraigsailDB
from web_app.app import create_app


@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / 'craigsail.db'
    db = CraigsailDB(str(db_path))

    db.save_listings(pd.DataFrame([
        {'id': '1', 'name': 'Cheap boat', 'url': 'http://x/1', 'city': 'sfbay',
         'price': '$1,000', 'where': 'sausalito', 'geotag': (37.85, -122.48), 'has_image': True},
        {'id': '2', 'name': 'Pricey boat', 'url': 'http://x/2', 'city': 'seattle',
         'price': '$9,000', 'where': 'ballard', 'geotag': (47.66, -122.38), 'has_image': True},
        {'id': '3', 'name': 'No location', 'url': 'http://x/3', 'city': 'sfbay',
         'price': '$500', 'where': 'oakland', 'geotag': None, 'has_image': False},
    ]), category='boo')

    app = create_app(db_path=str(db_path))
    app.config.update(TESTING=True)
    return app.test_client()


def test_index_renders(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<div id="map">' in response.data


def test_map_returns_only_geotagged_listings(client):
    payload = client.get('/map').get_json()

    assert payload['count'] == 2  # the un-geotagged listing is excluded
    names = {marker['name'] for marker in payload['markers']}
    assert names == {'Cheap boat', 'Pricey boat'}


def test_map_reports_price_range_for_colour_scale(client):
    payload = client.get('/map').get_json()
    assert payload['price_min'] == 1000.0
    assert payload['price_max'] == 9000.0


def test_map_centers_on_listings(client):
    payload = client.get('/map').get_json()
    latitude, longitude = payload['map_center']
    assert latitude == pytest.approx((37.85 + 47.66) / 2)
    assert longitude == pytest.approx((-122.48 + -122.38) / 2)


def test_map_filters_by_city(client):
    payload = client.get('/map?city=seattle').get_json()
    assert payload['count'] == 1
    assert payload['markers'][0]['name'] == 'Pricey boat'


def test_map_filters_by_category(client):
    assert client.get('/map?category=boo').get_json()['count'] == 2
    assert client.get('/map?category=bia').get_json()['count'] == 0


def test_categories_endpoint(client):
    payload = client.get('/categories').get_json()
    assert payload['categories'] == ['boo']
    assert payload['cities'] == ['seattle', 'sfbay']


def test_empty_database_is_handled(tmp_path):
    app = create_app(db_path=str(tmp_path / 'empty.db'))
    app.config.update(TESTING=True)
    payload = app.test_client().get('/map').get_json()

    assert payload['count'] == 0
    assert payload['markers'] == []
    assert payload['map_center'] == [37.7749, -122.4194]
