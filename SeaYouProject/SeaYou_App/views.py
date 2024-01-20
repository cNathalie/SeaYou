import os
import requests
from django.shortcuts import render
from dotenv import load_dotenv
from operator import itemgetter
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from SeaYou_Models.models import Waypoint, Ship, Route

load_dotenv()

# Create your views here.

def home(request):
    return render(request, "home.html")

def ships(request):
    all_ships = Ship.objects.all()

    paginator = Paginator(all_ships, 15)
    page = request.GET.get('page')

    try:
        ships = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        ships = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page
        ships = paginator.page(paginator.num_pages)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        ships = Ship.objects.filter(shipname__icontains=search_query.lower())

    waypoints = list(Waypoint.objects.values('waypointdescription', 'waypointlatitude', 'waypointlongitude'))
    context = {
        'waypoints': waypoints, 
        'ships': ships,
        'search_query': search_query
        }
    return render(request, "ships.html", context)

def shipVisits(request, ship_imo):
    ship = Ship.objects.get(imo=ship_imo)
    visits = Route.objects.filter(shipid=ship).order_by().distinct().values('visit', 'journey', 'routecategoryid','routecategoryid__routecategoryname', 'dockeddt')
    
    context = {
        'ship': ship,
        'visits' : visits
    }


    return render(request, 'ship-visits.html', context)

def get_routes_for_visit(request, ship_imo, visit_id, route_id):

    ship = Ship.objects.get(imo=ship_imo)
    routes = list(Route.objects.filter(shipid=ship, visit=visit_id, routecategoryid__routecategoryid=route_id).values( 'visit', 'journey', 'waypointid',
        'waypointid__waypointlatitude', 'waypointid__waypointlongitude', 'waypointid__waypointdescription', 'waypointdt', 'dockeddt', 'routecategoryid'))
    
    # Only one timestamp per waypoint needed
    unique_waypoint_ids = set()
    unique_routes = []

    for route in routes:
        waypoint_id = route['waypointid']
        if waypoint_id not in unique_waypoint_ids:
            unique_waypoint_ids.add(waypoint_id)
            unique_routes.append(route)
    
    unique_routes = sorted(unique_routes, key=itemgetter('waypointdt'))

    return JsonResponse(unique_routes, safe=False)



def weather(request):

    # get access token
    api_url = os.getenv("NXTPORT_GET_TOKEN")
    form_data = {
        "username" : os.getenv("NXTPORT_USERNAME"),
        "password" : os.getenv("NXTPORT_PASSWORD"),
        "grant_type" : "password",
        "client_id" : os.getenv("NXTPORT_ID"),
        "client_secret" : os.getenv("NXTPORT_SECRET"),
        "scope" : "openid"
    }

    response = requests.post(api_url, data=form_data)
    if response.status_code == 200:
        # Request was successful
        print("API call successful!")
        data = response.json()
        access_token = data.get("access_token")
        os.environ["NXTPORT_CURRENT_TOKEN"] = access_token
        print(access_token)  # Assuming the response is in JSON format
    else:
        # Handle errors
        print(f"API call failed with status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging

    
    # probeersel
    current_access_token = os.getenv("NXTPORT_CURRENT_TOKEN")
    weather_url = os.getenv("NXTPORT_METEO_URL")
    weather_params = {
        "location" : "k102",
        "subscription-key" : os.getenv("NXTPORT_METEO_SUBKEY")
    }
    weather_headers = {
        "Authorization" : "Bearer " + current_access_token,
        "Accept" : "*/*",
        "Accept-Encoding" : "gzip,deflate,br",
        "Connection" : "keep-alive",
        "Content-Type": "application/json",
    }

    weather_response = requests.get(weather_url, params=weather_params, headers=weather_headers)

    if weather_response.status_code == 200:
        # Request was successful
        print("API weather call successful!")
        weather_data = weather_response.json()
        print(weather_data)  # Assuming the response is in JSON format
    else:
        # Handle errors
        print(f"WEATHER API call failed with status code: {weather_response.status_code}")
        print(weather_response.text)  # Print the response content for debugging

    return render(request, 'weather.html')



def get_weather_for_station(request, station):

    return JsonResponse("")

def eta(request):
    return render(request, 'eta.html')

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, 'contact.html')