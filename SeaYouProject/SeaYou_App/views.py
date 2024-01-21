
import json
from django.shortcuts import render
from dotenv import load_dotenv
from operator import itemgetter
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from SeaYou_Models.models import Waypoint, Ship, Route, WeatherCache, ETACache

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
        # If page is out of range, deliver the last page
        ships = paginator.page(paginator.num_pages)

    # # Search functionality
    # search_query = request.GET.get('search', '')
    # if search_query:
    #     ships = Ship.objects.filter(shipname__icontains=search_query.lower())

    waypoints = list(Waypoint.objects.values('waypointdescription', 'waypointlatitude', 'waypointlongitude'))
    context = {
        'waypoints': waypoints, 
        'ships': ships,
        # 'search_query': search_query
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
    
    cashed_data = WeatherCache.objects.first()
    weather_data = cashed_data.cashed_weather_data
    updated_at = cashed_data.updated_at

    context: {
        'data' : weather_data,
        'timestamp' : updated_at
    }

    return render(request, 'weather.html', context)


def eta(request):

    eta_data = ETACache.objects.filter(name='BEANR').first().cashed_eta_data
    # Formatting as json:
    eta_formatted = eta_data.replace("'", '"').replace("None", '"Unknown"')
    # Converting to a dict
    data_dict = json.loads(eta_formatted)
    
    context = {
        'data' : data_dict
    }

    return render(request, 'eta.html', context)

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, 'contact.html')