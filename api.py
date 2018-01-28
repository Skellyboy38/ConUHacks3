from flask import Flask, jsonify, request, render_template
from googleplaces import GooglePlaces, types, lang
import urllib3
import json
import sys
from math import sin, cos, sqrt, atan2, radians

app = Flask(__name__, static_folder='public', static_url_path='/public')

'''
TODO
1) Issue with AJAX link
2) use domain name
3) UI (side buttons + main button, also it looks like crap)
4) Dias' thing with orientation if we have time??
'''


@app.route("/")
def hello():
    return render_template('index.html');


@app.route("/get_nearest_places", methods=['POST'])
def get_nearest_places(lat, lng, radius, auth_key):
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
    return places_to_ret

@app.route("/get_closest", methods=['POST'])
def get_closest():
    try:
        global closest_place_info
        auth_key = 'AIzaSyAJPbBg8lwlXpm_3k9voCLMQqMq5RutYdc'
        print(request.form)
        lat = request.form['latitude']
        lng = request.form['longitude']
        radius = request.form['radius']
        closest_distance = -1
        result = get_nearest_places(lat, lng, radius, auth_key)
        for x in result:
            place_lat = x["geo_location"]["latitude"]
            place_lng = x["geo_location"]["longitude"]
            R = 6373.0
            current_rad_lat = radians(float(lat))
            current_rad_lng = radians(float(lng))
            place_rad_lat = radians(float(place_lat))
            place_rad_lng = radians(float(place_lng))
            dlon = place_rad_lng - current_rad_lng
            dlat = place_rad_lat - current_rad_lat
            a = sin(dlat / 2) ** 2 + cos(current_rad_lat) * cos(current_rad_lng) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c
            if closest_distance == -1:
                closest_place_info = x
                closest_distance = distance
            elif distance < closest_distance:
                closest_place_info = x
                closest_distance = distance
        closest_result_info = {}
        closest_result_info['place_info']= closest_place_info
        closest_result_info['distance_km']= closest_distance
        closest_result_info['reviews']= _get_place_reviews(closest_place_info["id"], auth_key)
        return jsonify(closest_result_info)

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
