from flask import Flask, render_template, jsonify
import pandas as pd
from craigsail.search import Search

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/map')
def map_view():
    # Assuming you have a function to get search results
    search = Search(search_category='your_category', data_path='your_data_path', cities=['city1', 'city2'])
    _, results_df = search.get_all_daily_postings()

    # Prepare data for Leaflet map
    markers = []
    for _, row in results_df.iterrows():
        if 'geotag' in row and row['geotag']:
            markers.append({
                'location': row['geotag'],
                'popup': row['name']
            })

    # Respond to the AJAX request with JSON data
    return jsonify({
        'map_center': [37.7749, -122.4194],
        'markers': markers
    })

if __name__ == '__main__':
    app.run(debug=True)
