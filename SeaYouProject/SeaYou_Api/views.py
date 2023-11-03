from django.shortcuts import render
from rest_framework import viewsets
from SeaYou_Models.models import Ship, Routecategory, Zoneto, Waypoint, Route
from .serializers import ShipSerializer, RoutecategorySerializer, ZonetoSerializer, WaypointSerializer, RouteSerializer

# Create your views here.

class ShipViewSet(viewsets.ModelViewSet):
    queryset = Ship.objects.all()
    serializer_class = ShipSerializer

class RoutecategoryViewSet(viewsets.ModelViewSet):
    queryset = Routecategory.objects.all()
    serializer_class = RoutecategorySerializer

class ZonetoViewSet(viewsets.ModelViewSet):
    queryset = Zoneto.objects.all()
    serializer_class = ZonetoSerializer

class WaypointViewSet(viewsets.ModelViewSet):
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer