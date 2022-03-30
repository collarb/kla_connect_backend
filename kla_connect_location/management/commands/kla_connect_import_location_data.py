from django.core.management import BaseCommand
import pandas as pd
from kla_connect_location.models import Area

class Command(BaseCommand):
    help = "Import location data from an excel sheet"
    
    def add_arguments(self, parser):
        parser.add_argument("location",type=str, help="location data")
        parser.add_argument("sheet",type=str, help="location data")

    def handle(self, *args, **options):
        file_location = options['location']
        sheet_name = options['sheet']
        df = pd.read_excel(file_location, sheet_name)
        divisions = df['Division']
        parishes = df["Parish"]
        villages = df["Village"]
        streets = df["Street"]
        for i in range(len(divisions)):
            division, created = Area.objects.get_or_create(name__iexact=divisions[i].title(),parent__isnull=True)
            print(division,created)
            parish, _created = division.child_areas.get_or_create(name__iexact=parishes[i].title())
            print(parish,_created)
            village, __created = parish.child_areas.get_or_create(name__iexact=villages[i].title())
            print(village, __created)
            street, ___created = village.child_areas.get_or_create(name__iexact=streets[i].title())
            print(street, ___created)
            