from django.shortcuts import render
from django.http import JsonResponse
import cv2
import dlib
import numpy as np
import math
import geocoder
from geopy.geocoders import Nominatim
from geopy import Point
from geopy.exc import GeocoderTimedOut
import requests

# getting face detector and predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("V:/shape_predictor_68_face_landmarks.dat")

# euclidean distance(hypo distance btw 2 points by making right angle triangle)
def euclidean_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def faint_detection(request):
    if request.method == 'POST':
        # read frame from camera
        image = request.FILES['image']
        frame = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)

        # detect face landmarks using dlib
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        for face in faces:
            landmarks = predictor(gray, face)
            landmarks = np.array([[p.x, p.y] for p in landmarks.parts()])

            #distance btwn nose tip and chin
            nose_tip = landmarks[30]
            chin = landmarks[8]
            nose_chin_dist = euclidean_distance(nose_tip, chin)

            # distance btwn eyebrows and mouth
            eyebrows = landmarks[17:27]
            mouth = landmarks[48:68]
            eyebrows_mouth_dist = euclidean_distance(np.mean(eyebrows, axis=0), np.mean(mouth, axis=0))

            # check if the person is likely to faint based on facial landmarks
            if nose_chin_dist > eyebrows_mouth_dist:
                response = {
                    'status': 'Faint predicted'
                }
                return JsonResponse(response)

        response = {
            'status': 'No faint detected'
        }
        return JsonResponse(response)

    return render(request, 'faint_detector/faint_detection.html')

def get_current_coordinates():
    geolocator = Nominatim(user_agent="my-app")

    # Attempt to get the address using GPS coordinates
    try:
        g = geocoder.ip('me')
        location = geolocator.reverse(str(g.latlng[0]) + "," + str(g.latlng[1]))
        return (g.latlng[0], g.latlng[1])
    except GeocoderTimedOut:
        return None

    location = get_location()
    if location is not None:
        latitude, longitude = location
        print("Latitude:", latitude)
        print("Longitude:", longitude)
    else:
        print("Location not found")


coordinates, address = get_current_coordinates()
# the location may or may not be correct depending on the GPS data
# more accurate the data, more accurate the location

print(coordinates)
print(address)

####################################################################################################################

def find_nearby_places(latitude, longitude):
    # Define the API endpoint and parameters
    endpoint = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{latitude},{longitude}',
        'radius': '1000',
        'type': 'hospital|police',
        'key': 'YOUR_API_KEY_HERE'
    }

    # Send the API request
    response = requests.get(endpoint, params=params).json()

    # Parse the response and extract the relevant information
    nearby_places = []
    for result in response['results']:
        place = {
            'name': result['name'],
            'address': result['vicinity'],
            'location': result['geometry']['location'],
            'type': result['types'][0]
        }

        # this only happens IF there is any nearby place available
        nearby_places.append(place)

    return nearby_places

a, b = get_current_coordinates()

near = find_nearby_places(a, b)

print(near)

# (Error handling) Check if the request was successful
# if response.status_code != 200:
#     print(f"Error: Request failed with status code {response.status_code}")
# else:
#     # Extract the results from the response
#     results = response.json()["results"]
#
#     # Check if any results were found
#     if len(results) == 0:
#         print("No hospitals or police stations found within 5km of your location.")
#     else:
#         # Print the names and addresses of nearby hospitals and police stations
#         print("Nearby hospitals and police stations:")
#         for result in results:
#             print(result["name"])
#             print(result["vicinity"])