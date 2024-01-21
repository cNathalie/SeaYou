from django.apps import AppConfig
from . import tasks


class SeaYou_AppConfig(AppConfig):
    name = 'SeaYou_App'
    def ready(self):
        tasks.start()
