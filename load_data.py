import os
import sys
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kanji_app.settings')

# Initialize Django
django.setup()

import pandas as pd
from cards.models import Card

# Load data from the CSV file into a DataFrame
csv_file = "media/csvs/n1.csv"
df = pd.read_csv(csv_file)

# Iterate through the DataFrame and create Card instances
for _, row in df.iterrows():
    Card.objects.create(
        expression=row['expression'],
        reading=row['reading'],
        meaning=row['meaning'],
        tags=row['tags'],
    )
