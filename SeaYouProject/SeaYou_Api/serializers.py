from rest_framework import serializers
from SeaYou_Models.models import Ship, Routecategory, Zoneto, Waypoint, Route

class ShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ship
        fields = '__all__'

class RoutecategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Routecategory
        fields = '__all__'

class ZonetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zoneto
        fields = '__all__'

class WaypointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Waypoint
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'