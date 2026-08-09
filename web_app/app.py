"""
Flask app that maps stored craigslist listings.

Reads from the sqlite database populated by the craigsail CLI rather than
scraping on every request - a live multi-city scrape takes minutes and would
time out the browser.

Run:
    CRAIGSAIL_DB=data/craigsail.db flask --app web_app.app run
"""
import os

from flask import Flask, jsonify, render_template, request

from craigsail.db import CraigsailDB

# Fallback map centre (San Francisco) used when no listing has coordinates.
DEFAULT_CENTER = [37.7749, -122.4194]


def create_app(db_path=None):
    app = Flask(__name__)
    app.config['DB_PATH'] = db_path or os.environ.get('CRAIGSAIL_DB', 'data/craigsail.db')

    def get_db():
        return CraigsailDB(app.config['DB_PATH'])

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/categories')
    def categories():
        """
        Distinct category/city pairs, so the UI can offer real choices
        instead of hardcoded placeholders.
        """
        df = get_db().load_listings()
        if df.empty:
            return jsonify({'categories': [], 'cities': []})

        return jsonify({
            'categories': sorted(df['category'].dropna().unique().tolist()),
            'cities': sorted(df['city'].dropna().unique().tolist()),
        })

    @app.route('/map')
    def map_view():
        """
        GeoJSON-ish marker payload for Leaflet, filtered by optional
        ?category= and ?city= query params.
        """
        df = get_db().load_listings(
            category=request.args.get('category'),
            city=request.args.get('city'),
            with_geo_only=True,
        )

        if df.empty:
            return jsonify({'map_center': DEFAULT_CENTER, 'markers': [], 'count': 0})

        prices = df['price'].dropna()
        price_min = float(prices.min()) if not prices.empty else None
        price_max = float(prices.max()) if not prices.empty else None

        markers = []
        for _, row in df.iterrows():
            price = None if row['price'] is None or row['price'] != row['price'] else float(row['price'])
            markers.append({
                'location': [float(row['latitude']), float(row['longitude'])],
                'name': row['name'],
                'url': row['url'],
                'city': row['city'],
                'price': price,
                'where': row['where_'],
            })

        return jsonify({
            'map_center': [float(df['latitude'].mean()), float(df['longitude'].mean())],
            'markers': markers,
            'count': len(markers),
            'price_min': price_min,
            'price_max': price_max,
        })

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
