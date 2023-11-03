from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShipViewSet, RoutecategoryViewSet, ZonetoViewSet, WaypointViewSet, RouteViewSet

# router = DefaultRouter()
# router.register(r'ships', ShipViewSet)
# router.register(r'routecategories', RoutecategoryViewSet)
# router.register(r'zones', ZonetoViewSet)
# router.register(r'waypoints', WaypointViewSet)
# router.register(r'routes', RouteViewSet)

urlpatterns = [
    path('api/ships', ShipViewSet.as_view({'get': 'list'}), name='ships-list'),
    path('api/routecategories', RoutecategoryViewSet.as_view({'get': 'list'}), name='routecategories-list'),
    path('api/zones', ZonetoViewSet.as_view({'get': 'list'}), name='zones-list'),
    path('api/waypoints', WaypointViewSet.as_view({'get': 'list'}), name='waypoints-list'),
    path('api/routes', RouteViewSet.as_view({'get': 'list'}), name='routes-list')
]
