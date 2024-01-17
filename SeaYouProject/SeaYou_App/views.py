from django.shortcuts import render
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

def shipRoute(request, ship_imo):
    ship = Ship.objects.get(imo=ship_imo)
    routes = Route.objects.filter(shipid=ship)

    context = {
        'ship': ship,
        'routes' : routes
    }
    return render(request, 'ship-route.html', context)

def weather(request):
    return render(request, 'weather.html')

def eta(request):
    return render(request, 'eta.html')

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, 'contact.html')