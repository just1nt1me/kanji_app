import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from level_test.models import Kanji, JLPTLevel

class Command(BaseCommand):
    help = 'Load Kanji data from CSV files into the database'

    def handle(self, *args, **options):
        # Define the directory where your CSV files are located
        csv_directory = os.path.join(settings.MEDIA_ROOT, 'csvs')

        # Load data from CSV files and populate the database
        for csv_file in ["n1.csv", "n2.csv", "n3.csv", "n4.csv", "n5.csv"]:
            csv_path = os.path.join(csv_directory, csv_file)
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                jlpt_level, _ = JLPTLevel.objects.get_or_create(level=csv_file.split(".")[0])
                for row in csv_reader:
                    Kanji.objects.create(
                        expression=row['expression'],
                        reading=row['reading'],
                        meaning=row['meaning'],
                        tags=jlpt_level
                    )
                print(f"Loaded {csv_file} to database")
