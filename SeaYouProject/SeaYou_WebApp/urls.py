from django.urls import path
from SeaYou_WebApp import views as app_views


urlpatterns = [
    path("", app_views.home, name="home" )
]
