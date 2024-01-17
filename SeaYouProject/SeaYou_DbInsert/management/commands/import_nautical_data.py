import decimal
from datetime import datetime
import pandas as pd
from django.core.management.base import BaseCommand
from SeaYou_Models.models import Ship, Routecategory, Zoneto, Waypoint, Route
import os
import pytz
from django.conf import settings
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Import data from Excel into the database'
    print("Current Working Directory:", os.getcwd())

    def handle(self, *args, **options):
        excel_file_path = './SeaYou_DbInsert/data/Aankomst.xlsx'
        df = pd.read_excel(excel_file_path)

        for index, row in df.iterrows():
            self.stdout.write(self.style.SUCCESS(f"Processing line {index + 1}"))

            ship_imo = row['IMO nummer']
            ship_visit = row['Verblijf']
            ship_journey = row['Reis']
            ship_name = row['Schip']
            route_category_name = row['Route categorie']
            zone_to_name = row['Zone naar']
            waypoint_name = row['Locatie']
            route_started_str = row['Aanvang tijd']
            passage_time_str = row['Passage tijd']
            docked_time_str = row['Gemeerd tijd']

            # Leave out unidentified ships
            if pd.isna(row['IMO nummer']):
                self.stdout.write(self.style.WARNING(f"Skipping route creation for line {index + 1}, ship_imo is NaN."))
                continue

            # Check if Waypoint in db
            try:
                waypoint = Waypoint.objects.get(waypointname=waypoint_name)
                
            except Waypoint.DoesNotExist:
                # Skip creating Route if Waypoint not in db
                self.stdout.write(self.style.WARNING(f"Skipping route creation for {waypoint_name}, Waypoint not found."))
                continue

            self.stdout.write(self.style.SUCCESS(f"Waypoint found: {waypoint_name} = {waypoint.waypointname}"))

            # Check if Ship exists
            ship, created = Ship.objects.get_or_create(
                imo=ship_imo,
                defaults={
                    'shipname': ship_name,
                    'max_length': decimal.Decimal(str(row['Max lengte']).replace(',', '.')),
                    'max_width': decimal.Decimal(str(row['Max breedte']).replace(',', '.')),
                    'max_draft': decimal.Decimal(str(row['Max diepgang']).replace(',', '.')),
                    'operationaldraft': decimal.Decimal(str(row['Operationele diepgang']).replace(',', '.')),
                }
            )

            self.stdout.write(self.style.SUCCESS(f"Ship found/created: {ship.shipname}"))

            # Check if RouteCategory exists
            route_category, created = Routecategory.objects.get_or_create(
                routecategoryname=route_category_name
            )

            # Check if ZoneTo exists
            zone_to, created = Zoneto.objects.get_or_create(
                zonetoname=zone_to_name
            )

            # Convert to datatime
            # route_started_time = pd.to_datetime(route_started_str)
            # passage_time = pd.to_datetime(passage_time_str)
            # docked_time = pd.to_datetime(docked_time_str)
            # Convert to datetime, handling NaN values
            route_started_time = pd.to_datetime(route_started_str, errors='coerce')
            passage_time = pd.to_datetime(passage_time_str, errors='coerce')
            docked_time = pd.to_datetime(docked_time_str, errors='coerce')

            # Convert NaT to None
            route_started_time = route_started_time if not pd.isna(route_started_time) else None
            passage_time = passage_time if not pd.isna(passage_time) else None
            docked_time = docked_time if not pd.isna(docked_time) else None

             # Check if Route already exists
            existing_route = Route.objects.filter(
                shipid=ship,
                waypointid=waypoint,
                routestarteddt=route_started_time
            ).first()

            if existing_route:
                self.stdout.write(self.style.WARNING(f"Skipping route creation for line {index + 1}, Route already exists."))
                continue

            # Create Route object
            route = Route.objects.create(
                visit=ship_visit,
                journey=ship_journey,
                shipid=ship,
                routecategoryid=route_category,
                routestarteddt=route_started_time,
                waypointid=waypoint,
                waypointdt=passage_time,
                dockeddt=docked_time,
                zonetoid=zone_to,
            )

            self.stdout.write(self.style.SUCCESS(f"Route {route.routeid} in database"))
