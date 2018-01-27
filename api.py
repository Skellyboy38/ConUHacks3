from flask import Flask, jsonify, request
from googleplaces import GooglePlaces, types, lang
import urllib3
import json
import sys
app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({'status': 'success'})


@app.route("/get_nearest_places", methods=['POST'])
def get_nearest_places():
    try:
        auth_key = request.form['key']
        lat = request.form['latitude']
        lng = request.form['longitude']
        radius = request.form['radius']
        google_places = GooglePlaces(auth_key)

        query_result = google_places.nearby_search(
            radius=int(radius), types=[types.TYPE_RESTAURANT],
            lat_lng={'lat': lat, 'lng': lng}
        )
        places_to_ret = []
        for place in query_result.places:
            places_to_ret.append({
                'name': str(place.name),
                'geo_location': {
                    'latitude': str(place.geo_location['lat']),
                    'longitude': str(place.geo_location['lng'])
                },
                'id': str(place.place_id)
            })
        return jsonify(places_to_ret)

    except Exception as e:
        print(str(e), file=sys.stderr)
        return jsonify({'status': 'error', 'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
