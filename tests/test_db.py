import pandas as pd
import pytest

from craigsail.db import CraigsailDB, _parse_geotag


@pytest.fixture
def db(tmp_path):
    return CraigsailDB(str(tmp_path / 'craigsail.db'))


def listing(listing_id='7612345678', price='$1,000', name='Catalina 30', geotag=(37.77, -122.41)):
    return pd.DataFrame([{
        'id': listing_id,
        'name': name,
        'url': 'https://sfbay.craigslist.org/boo/123.html',
        'city': 'sfbay',
        'price': price,
        'where': 'sausalito',
        'geotag': geotag,
        'has_image': True,
        'datetime': '2026-08-01 10:00',
        'length overall (LOA)': '30',
    }])


def test_tables_created(db):
    with db.connect() as conn:
        names = {row['name'] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
    assert {'listings', 'price_history'} <= names


def test_save_listings_inserts_and_parses(db):
    inserted, updated, changes = db.save_listings(listing(), category='boo')

    assert (inserted, updated, changes) == (1, 0, 1)

    saved = db.load_listings()
    assert len(saved) == 1
    assert saved['price'].iloc[0] == 1000.0
    assert saved['latitude'].iloc[0] == pytest.approx(37.77)
    assert saved['longitude'].iloc[0] == pytest.approx(-122.41)
    assert saved['category'].iloc[0] == 'boo'


def test_rerunning_same_search_does_not_duplicate(db):
    db.save_listings(listing(), category='boo')
    inserted, updated, changes = db.save_listings(listing(), category='boo')

    assert inserted == 0
    assert updated == 1
    assert changes == 0  # price unchanged, so no new observation
    assert len(db.load_listings()) == 1


def test_price_change_is_recorded(db):
    db.save_listings(listing(price='$1,000'), category='boo')
    db.save_listings(listing(price='$900'), category='boo')

    history = db.price_history('7612345678')
    assert list(history['price']) == [1000.0, 900.0]

    drops = db.price_drops()
    assert len(drops) == 1
    assert drops['change'].iloc[0] == -100.0


def test_non_core_columns_land_in_attributes(db):
    db.save_listings(listing(), category='boo')
    attrs = db.load_listings()['attributes'].iloc[0]
    assert 'length overall (LOA)' in attrs


def test_listing_without_id_is_skipped(db):
    df = pd.DataFrame([{'id': None, 'name': 'no id', 'price': '$5'}])
    inserted, updated, changes = db.save_listings(df, category='boo')
    assert (inserted, updated, changes) == (0, 0, 0)


def test_load_listings_filters(db):
    db.save_listings(listing(listing_id='1'), category='boo')
    db.save_listings(listing(listing_id='2'), category='bia')

    assert len(db.load_listings(category='boo')) == 1
    assert len(db.load_listings(city='sfbay')) == 2
    assert len(db.load_listings(city='seattle')) == 0


def test_missing_geotag_is_tolerated(db):
    db.save_listings(listing(geotag=None), category='boo')
    saved = db.load_listings()
    assert pd.isna(saved['latitude'].iloc[0])
    assert len(db.load_listings(with_geo_only=True)) == 0


@pytest.mark.parametrize('raw,expected', [
    ((37.77, -122.41), (37.77, -122.41)),
    ('(37.77, -122.41)', (37.77, -122.41)),
    ([37.77, -122.41], (37.77, -122.41)),
    (None, (None, None)),
    ('not a geotag', (None, None)),
    ((1, 2, 3), (None, None)),
])
def test_parse_geotag(raw, expected):
    assert _parse_geotag(raw) == expected


def test_unparseable_price_becomes_null(db):
    db.save_listings(listing(price='please call'), category='boo')
    assert pd.isna(db.load_listings()['price'].iloc[0])
