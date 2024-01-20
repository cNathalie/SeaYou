from django.urls import path
from SeaYou_App import views as app_views


urlpatterns = [
    # For web-client
    path("", app_views.home, name="home" ),
    path("ships", app_views.ships, name="ships"),
    path("ship-visits/<int:ship_imo>", app_views.shipVisits, name="shipVisits"),
    path("weather", app_views.weather, name="weather"),
    path("eta", app_views.eta, name="eta"),
    path("about", app_views.about, name= 'about'),
    path("contact", app_views.contact, name='contact'),
    # For additional data
    path('api/get_routes_for_visit/<str:ship_imo>/<str:visit_id>/', app_views.get_routes_for_visit, name='get_routes_for_visit'),
]
