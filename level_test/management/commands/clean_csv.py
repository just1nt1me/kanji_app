import os
import pandas as pd
import re
from django.core.management.base import BaseCommand
# from kanji_test.models import Kanji, JLPTLevel  # Import your models here

# Function to check if a string contains kanji
def contains_kanji_or_hiragana(text):
    kanji_or_hiragana_pattern = re.compile(r'[\u4e00-\u9fafぁ-ゞ]+.*[\u4e00-\u9faf]+|[\u4e00-\u9faf]+')
    return bool(kanji_or_hiragana_pattern.search(text))

class Command(BaseCommand):
    help = 'Clean and update CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-directory',
            default='media/csvs/',  # Change this path to match your CSV directory
            help='Specify the directory where CSV files are located'
        )

    def handle(self, *args, **options):
        csv_directory = options['csv_directory']

        for csv_file in os.listdir(csv_directory):
            if csv_file.endswith('.csv'):
                csv_path = os.path.join(csv_directory, csv_file)

                # Check if the CSV file exists
                if os.path.exists(csv_path):
                    level = csv_file.split('.')[0]
                    df = pd.read_csv(csv_path)

                    # Drop duplicates based on the 'expression' column
                    df = df.drop_duplicates(subset=["expression"])

                    # Update the 'tags' column with JLPT level
                    df['tags'] = level
                    df = df[['expression', 'reading', 'meaning', 'tags']]
                    # Clean the 'reading' and 'meaning' columns
                    characters_to_remove = r'[～\(\)\.\;\-\~]'
                    df['reading'] = df['reading'].str.replace(characters_to_remove, '')
                    df['meaning'] = df['meaning'].str.replace(characters_to_remove, '')

                    # Remove kanji, hiragana, and katakana characters from the 'meaning' column
                    kanji_hiragana_katakana = r'[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]'
                    df['meaning'] = df['meaning'].apply(lambda x: re.sub(kanji_hiragana_katakana, '', x))

                    # Remove standalone occurrences of "vt", "vi", "eg", "to"
                    standalone = r'\b(vt|vi|eg|to)\b'
                    df['meaning'] = df['meaning'].str.replace(standalone, '', regex=True)
                    df['meaning'] = df['meaning'].apply(lambda x: x.lower())

                    # Create a mask to filter rows containing kanji or hiragana
                    mask = df['expression'].apply(lambda x: contains_kanji_or_hiragana(x))
                    df = df[mask]

                    # Save the cleaned CSV back to the original file
                    df.to_csv(csv_path, index=False)

                    self.stdout.write(self.style.SUCCESS(f'Successfully cleaned and updated {csv_file}'))
                else:
                    self.stdout.write(self.style.WARNING(f'CSV file {csv_file} not found in {csv_directory}'))
