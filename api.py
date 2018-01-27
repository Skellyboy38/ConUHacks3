from flask import Flask, jsonify, request, render_template
from googleplaces import GooglePlaces, types, lang
import urllib3
import json
import sys
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html');


@app.route("/get_nearest_places", methods=['POST'])
def get_nearest_places():
    try:
        auth_key = 'AIzaSyAJPbBg8lwlXpm_3k9voCLMQqMq5RutYdc'
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
        return jsonify({'status': 'error', 'error': str(e)})


def _get_place_reviews(place_id, key):
    url = "https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}".format(place_id, key)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    return json.loads(response.data.decode('utf-8'))['result']['reviews']


if __name__ == "__main__":
    app.run(debug=True)
