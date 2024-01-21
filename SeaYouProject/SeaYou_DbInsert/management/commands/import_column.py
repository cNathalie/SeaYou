from typing import Any
from django.core.management.base import BaseCommand
import pandas as panda
from SeaYou_Models.models import Ship, Zoneto, Waypoint, Route, Routecategory

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('excel_file_path', type=str)
        parser.add_argument('sheet_name', type=str)
        parser.add_argument('column_name', type=str)
    
    def handle(self, *args: Any, **options):
        excel_file_path = options['excel_file_path']
        sheet_name = options['sheet_name']
        column_name = options['column_name']

        try:
            data_file = panda.read_excel(excel_file_path, sheet_name=sheet_name)

            if column_name in data_file.columns:
                column_data = data_file[column_name]


                unique_values = column_data.drop_duplicates()

                list = unique_values.tolist()

                for value in unique_values:
                    if not Waypoint.objects.filter(waypointname=value).exists():
                        Waypoint.objects.create(waypointname=value)
                        self.stdout.write(self.style.SUCCESS(f'{value} imported in to db'))

                self.stdout.write(self.style.SUCCESS('Data import successful'))
                self.stdout.write(self.style.SUCCESS(list))

            else: 
                self.stdout.write(self.style.ERROR(f'Column "{column_name}" not found in the Excel sheet.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing the specified column to the database: {str(e)}'))