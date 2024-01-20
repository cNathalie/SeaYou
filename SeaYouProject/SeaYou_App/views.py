from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from SeaYou_Models.models import Waypoint, Ship, Route

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
    visits = Route.objects.filter(shipid=ship).order_by().distinct().values('visit', 'journey', 'routecategoryid__routecategoryname', 'dockeddt')

    routes = list(Route.objects.filter(shipid=ship).values( 'visit', 'journey', 'waypointid',
        'waypointid__waypointlatitude', 'waypointid__waypointlongitude', 'waypointid__waypointdescription', 'waypointdt', 'dockeddt', 'routecategoryid'))

    # Only one timestamp per waypoint needed
    unique_waypoint_ids = set()
    unique_routes = []

    for route in routes:
        waypoint_id = route['waypointid']
        if waypoint_id not in unique_waypoint_ids:
            unique_waypoint_ids.add(waypoint_id)
            unique_routes.append(route)
    
    context = {
        'ship': ship,
        'routes' : unique_routes,
        'visits' : visits
    }


    return render(request, 'ship-visits.html', context)

def get_routes_for_visit(request, ship_imo, visit_id):
    ship = Ship.objects.get(imo=ship_imo)
    routes = list(Route.objects.filter(shipid=ship, visit=visit_id).values( 'visit', 'journey', 'waypointid',
        'waypointid__waypointlatitude', 'waypointid__waypointlongitude', 'waypointid__waypointdescription', 'waypointdt', 'dockeddt', 'routecategoryid'))
    
    # Only one timestamp per waypoint needed
    unique_waypoint_ids = set()
    unique_routes = []

    for route in routes:
        waypoint_id = route['waypointid']
        if waypoint_id not in unique_waypoint_ids:
            unique_waypoint_ids.add(waypoint_id)
            unique_routes.append(route)
    

    return JsonResponse(unique_routes, safe=False)

def weather(request):
    return render(request, 'weather.html')

def eta(request):
    return render(request, 'eta.html')

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, 'contact.html')