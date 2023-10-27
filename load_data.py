import os
import django
import pandas as pd
from django.db import transaction
from level_test.models import Kanji

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kanji_app.settings')

# Initialize Django
django.setup()

# Assuming the CSV files are in the same directory as your script
current_directory = os.path.dirname(os.path.abspath(__file__))
csv_directory = os.path.join(current_directory, "media/csvs")
csv_list = [os.path.join(csv_directory, csv_name) for csv_name in ["n1.csv", "n2.csv", "n3.csv", "n4.csv", "n5.csv"]]

@transaction.atomic  # This ensures all changes in this function are atomic
def load_data_from_csv(csv_file):
    df = pd.read_csv(csv_file)

    # Iterate through the DataFrame
    for _, row in df.iterrows():
        # Fetch existing kanji with the same expression if exists
        kanji_instance, created = Kanji.objects.get_or_create(expression=row['expression'])

        # Update fields
        kanji_instance.reading = row['reading']
        kanji_instance.meaning = row['meaning']
        kanji_instance.tags = row['tags']

        # Save the changes
        try:
            kanji_instance.save()
        except Exception as e:
            print(f"Error saving {row['expression']}: {e}")

# Process each CSV file
for csv_file in csv_list:
    try:
        load_data_from_csv(csv_file)
        print(f"Processed {csv_file} successfully.")
    except Exception as e:
        print(f"Error processing {csv_file}: {e}")

print("Data loading completed.")
