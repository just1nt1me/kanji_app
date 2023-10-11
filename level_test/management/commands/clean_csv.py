# from nltk.corpus import wordnet
# from nltk.tokenize import word_tokenize
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

                    # Create a mask to filter rows containing kanji or hiragana
                    mask = df['expression'].apply(lambda x: contains_kanji_or_hiragana(x))
                    df = df[mask]

                    # Save the cleaned CSV back to the original file
                    df.to_csv(csv_path, index=False)

                    self.stdout.write(self.style.SUCCESS(f'Successfully cleaned and updated {csv_file}'))
                else:
                    self.stdout.write(self.style.WARNING(f'CSV file {csv_file} not found in {csv_directory}'))



# Define a function to compute WordNet-based similarity
def wordnet_similarity(user_input, correct_answer):
    user_tokens = word_tokenize(user_input)
    answer_tokens = word_tokenize(correct_answer)

    # Initialize a list to store individual word similarities
    word_similarities = []

    for user_word in user_tokens:
        max_similarity = 0  # Initialize max similarity for the current user word

        for answer_word in answer_tokens:
            user_synsets = wordnet.synsets(user_word)
            answer_synsets = wordnet.synsets(answer_word)

            if user_synsets and answer_synsets:
                similarity = max(
                    s1.wup_similarity(s2) for s1 in user_synsets for s2 in answer_synsets
                )

                if similarity > max_similarity:
                    max_similarity = similarity

        word_similarities.append(max_similarity)

    # Calculate the average similarity across all user words
    if word_similarities:
        average_similarity = sum(word_similarities) / len(word_similarities)
        return average_similarity
    else:
        return 0
