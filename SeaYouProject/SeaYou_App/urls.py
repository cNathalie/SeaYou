from django.urls import path
from SeaYou_App import views as app_views


urlpatterns = [
    path("", app_views.home, name="home" ),
    path("ships", app_views.ships, name="ships"),
    path("ship-route/<int:ship_imo>", app_views.shipRoute, name="shipRoute"),
    path("weather", app_views.weather, name="weather"),
    path("eta", app_views.eta, name="eta"),
    path("about", app_views.about, name= 'about'),
    path("contact", app_views.contact, name='contact')
]
