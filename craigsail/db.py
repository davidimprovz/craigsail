"""
sqlite3 persistence for craigsail.

Two tables:

  listings      one row per craigslist posting, keyed by the craigslist id.
                Re-running a search updates the existing row rather than
                appending a duplicate.

  price_history one row per (listing, price) change, appended only when the
                price actually moves. This is what backs price tracking and
                buy-level alerts.
"""
from contextlib import contextmanager
from pathlib import Path
import json
import sqlite3

import pandas as pd

# Columns promoted out of the craigslist payload into real table columns.
# Anything else the API returns is kept in the `attributes` JSON blob so we
# never silently drop data.
CORE_COLUMNS = [
    'id',
    'name',
    'url',
    'city',
    'category',
    'price',
    'where',
    'geotag',
    'latitude',
    'longitude',
    'has_image',
    'datetime',
    'last_updated',
    'created',
    'repost_of',
    'body',
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS listings (
    id            TEXT PRIMARY KEY,
    name          TEXT,
    url           TEXT,
    city          TEXT,
    category      TEXT,
    price         REAL,
    where_        TEXT,
    geotag        TEXT,
    latitude      REAL,
    longitude     REAL,
    has_image     INTEGER,
    datetime      TEXT,
    last_updated  TEXT,
    created       TEXT,
    repost_of     TEXT,
    body          TEXT,
    attributes    TEXT,
    first_seen    TEXT NOT NULL,
    last_seen     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_listings_city     ON listings (city);
CREATE INDEX IF NOT EXISTS idx_listings_category ON listings (category);
CREATE INDEX IF NOT EXISTS idx_listings_price    ON listings (price);

CREATE TABLE IF NOT EXISTS price_history (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    listing_id TEXT NOT NULL,
    price      REAL,
    observed   TEXT NOT NULL,
    FOREIGN KEY (listing_id) REFERENCES listings (id)
);

CREATE INDEX IF NOT EXISTS idx_price_history_listing ON price_history (listing_id);
"""


def _parse_geotag(geotag):
    """
    craigslist returns geotag as a (lat, lon) tuple, or None. Accept the
    string form too, since a round-trip through CSV stringifies it.
    """
    if geotag is None or (not isinstance(geotag, (list, tuple)) and pd.isna(geotag)):
        return None, None

    if isinstance(geotag, str):
        try:
            geotag = json.loads(geotag.replace('(', '[').replace(')', ']'))
        except (ValueError, TypeError):
            return None, None

    if isinstance(geotag, (list, tuple)) and len(geotag) == 2:
        try:
            return float(geotag[0]), float(geotag[1])
        except (TypeError, ValueError):
            return None, None

    return None, None


class CraigsailDB:
    """
    Thin wrapper over a sqlite3 database file.

    Usage:
        db = CraigsailDB('data/craigsail.db')
        db.save_listings(df, category='boo')
        db.price_history('7612345678')
    """

    def __init__(self, db_path):
        self.db_path = Path(db_path)
        if self.db_path.parent != Path(''):
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.create_tables()

    @contextmanager
    def connect(self):
        """
        Yield a connection that commits on success and rolls back on error.
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def create_tables(self):
        with self.connect() as conn:
            conn.executescript(SCHEMA)

    def _to_records(self, df, category):
        """
        Reshape a search DataFrame into rows matching the listings table.
        Unknown columns are folded into the `attributes` JSON blob.
        """
        now = pd.Timestamp.utcnow().isoformat()
        records = []

        for _, row in df.iterrows():
            data = row.to_dict()

            listing_id = data.get('id')
            if listing_id is None or (not isinstance(listing_id, (list, tuple)) and pd.isna(listing_id)):
                continue  # cannot dedupe without an id

            latitude, longitude = _parse_geotag(data.get('geotag'))

            price = data.get('price')
            if isinstance(price, str):
                price = price.replace('$', '').replace(',', '').strip()
            try:
                price = float(price) if price not in (None, '') and not pd.isna(price) else None
            except (TypeError, ValueError):
                price = None

            extras = {
                key: value for key, value in data.items()
                if key not in CORE_COLUMNS
            }

            records.append({
                'id': str(listing_id),
                'name': data.get('name'),
                'url': data.get('url'),
                'city': data.get('city'),
                'category': category,
                'price': price,
                'where_': data.get('where'),
                'geotag': json.dumps(data.get('geotag')) if data.get('geotag') is not None else None,
                'latitude': latitude,
                'longitude': longitude,
                'has_image': int(bool(data.get('has_image'))),
                'datetime': str(data.get('datetime')) if data.get('datetime') is not None else None,
                'last_updated': str(data.get('last_updated')) if data.get('last_updated') is not None else None,
                'created': str(data.get('created')) if data.get('created') is not None else None,
                'repost_of': str(data.get('repost_of')) if data.get('repost_of') is not None else None,
                'body': data.get('body'),
                'attributes': json.dumps(extras, default=str),
                'first_seen': now,
                'last_seen': now,
            })

        return records

    def save_listings(self, df, category):
        """
        Upsert listings, recording a price_history row whenever a listing is
        new or its price has changed. Returns (inserted, updated, price_changes).
        """
        assert isinstance(df, pd.DataFrame), f'df must be a pandas DataFrame. Got {type(df)}.'

        records = self._to_records(df, category)
        if not records:
            return 0, 0, 0

        inserted = updated = price_changes = 0

        with self.connect() as conn:
            for record in records:
                existing = conn.execute(
                    'SELECT id, price FROM listings WHERE id = ?', (record['id'],)
                ).fetchone()

                if existing is None:
                    conn.execute(
                        """
                        INSERT INTO listings (
                            id, name, url, city, category, price, where_, geotag,
                            latitude, longitude, has_image, datetime, last_updated,
                            created, repost_of, body, attributes, first_seen, last_seen
                        ) VALUES (
                            :id, :name, :url, :city, :category, :price, :where_, :geotag,
                            :latitude, :longitude, :has_image, :datetime, :last_updated,
                            :created, :repost_of, :body, :attributes, :first_seen, :last_seen
                        )
                        """,
                        record,
                    )
                    inserted += 1
                    conn.execute(
                        'INSERT INTO price_history (listing_id, price, observed) VALUES (?, ?, ?)',
                        (record['id'], record['price'], record['last_seen']),
                    )
                    price_changes += 1
                else:
                    conn.execute(
                        """
                        UPDATE listings SET
                            name = :name, url = :url, city = :city, category = :category,
                            price = :price, where_ = :where_, geotag = :geotag,
                            latitude = :latitude, longitude = :longitude,
                            has_image = :has_image, datetime = :datetime,
                            last_updated = :last_updated, created = :created,
                            repost_of = :repost_of, body = :body,
                            attributes = :attributes, last_seen = :last_seen
                        WHERE id = :id
                        """,
                        record,
                    )
                    updated += 1

                    if existing['price'] != record['price']:
                        conn.execute(
                            'INSERT INTO price_history (listing_id, price, observed) VALUES (?, ?, ?)',
                            (record['id'], record['price'], record['last_seen']),
                        )
                        price_changes += 1

        return inserted, updated, price_changes

    def load_listings(self, category=None, city=None, with_geo_only=False):
        """
        Read listings back as a DataFrame.
        """
        query = 'SELECT * FROM listings WHERE 1=1'
        params = []

        if category:
            query += ' AND category = ?'
            params.append(category)
        if city:
            query += ' AND city = ?'
            params.append(city)
        if with_geo_only:
            query += ' AND latitude IS NOT NULL AND longitude IS NOT NULL'

        with self.connect() as conn:
            return pd.read_sql_query(query, conn, params=params)

    def price_history(self, listing_id):
        """
        Full observed price trail for a single listing, oldest first.
        """
        with self.connect() as conn:
            return pd.read_sql_query(
                'SELECT price, observed FROM price_history '
                'WHERE listing_id = ? ORDER BY observed ASC',
                conn,
                params=[str(listing_id)],
            )

    def price_drops(self, category=None):
        """
        Listings whose latest price is below their first observed price -
        the buy-signal query the README describes.
        """
        query = """
        SELECT
            l.id, l.name, l.url, l.city, l.price AS current_price,
            first.price AS first_price,
            (l.price - first.price) AS change
        FROM listings l
        JOIN (
            SELECT listing_id, price
            FROM price_history ph
            WHERE ph.id = (
                SELECT MIN(id) FROM price_history WHERE listing_id = ph.listing_id
            )
        ) first ON first.listing_id = l.id
        WHERE l.price IS NOT NULL
          AND first.price IS NOT NULL
          AND l.price < first.price
        """
        params = []
        if category:
            query += ' AND l.category = ?'
            params.append(category)
        query += ' ORDER BY change ASC'

        with self.connect() as conn:
            return pd.read_sql_query(query, conn, params=params)
