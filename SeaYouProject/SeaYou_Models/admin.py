from django.contrib import admin
from .models import Ship, Routecategory, Zoneto, Waypoint, Route

# Register your models here.
admin.site.register(Ship)
admin.site.register(Routecategory)
admin.site.register(Zoneto)
admin.site.register(Waypoint)
admin.site.register(Route)
