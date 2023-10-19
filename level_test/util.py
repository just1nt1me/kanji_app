import pandas as pd
import re
import spacy
# from nltk.corpus import wordnet
# from nltk.tokenize import word_tokenize

csv_list = ["n1.csv", "n2.csv", "n3.csv", "n4.csv", "n5.csv"]

# Function to check if a string contains kanji
def contains_kanji_or_hiragana(text):
    # Use a regular expression to match kanji and hiragana characters
    kanji_or_hiragana_pattern = re.compile(r'[\u4e00-\u9fafぁ-ゞ]+.*[\u4e00-\u9faf]+|[\u4e00-\u9faf]+')
    return bool(kanji_or_hiragana_pattern.search(text))

# clean up csv and output
def clean_csv(csv):
    level = csv.split('.')[0]                                                       # get the JLPT level from the file name
    df = pd.DataFrame(pd.read_csv(csv))
    df = df.drop_duplicates(subset=["expression"])                                  # drop any rows that are duplicate expressions
    df.tags = level                                                                 # change all tags to be the JLPT level name
    df = df[['expression', 'reading', 'meaning', 'tags']]
    characters_to_remove = r'[～\(\)\.\;\-\~]'                                      # Define the characters you want to remove
    df['reading'] = df['reading'].str.replace(characters_to_remove, '')             # Apply the .str.replace() method to the specified columns
    df['meaning'] = df['meaning'].str.replace(characters_to_remove, '')
    mask = df['expression'].apply(lambda x: contains_kanji_or_hiragana(x))          # Apply the function and create a boolean mask
    df = df[mask]                                                                   # Filter the DataFrame to keep rows with kanji or a mix of kanji and hiragana
    df.to_csv(csv, index=False)                                               # output the cleaned csv to the original file

def main():
    for csv in csv_list:
        clean_csv(csv)

# Define a function to compute WordNet-based similarity
# def wordnet_similarity(user_input, correct_answer):
#     user_tokens = word_tokenize(user_input)
#     answer_tokens = word_tokenize(correct_answer)

#     # Initialize a list to store individual word similarities
#     word_similarities = []

#     for user_word in user_tokens:
#         max_similarity = 0  # Initialize max similarity for the current user word

#         for answer_word in answer_tokens:
#             user_synsets = wordnet.synsets(user_word)
#             answer_synsets = wordnet.synsets(answer_word)

#             if user_synsets and answer_synsets:
#                 similarity = max(
#                     s1.wup_similarity(s2) for s1 in user_synsets for s2 in answer_synsets
#                 )

#                 if similarity > max_similarity:
#                     max_similarity = similarity

#         word_similarities.append(max_similarity)

#     # Calculate the average similarity across all user words
#     if word_similarities:
#         average_similarity = sum(word_similarities) / len(word_similarities)
#         return average_similarity
#     else:
#         return 0

# Load a spaCy model (for English in this case)
nlp = spacy.load("en_core_web_md")

def spacy_similarity(user_input, correct_answer):
    user_tokens = nlp(user_input)
    answer_tokens = nlp(correct_answer)

    word_similarities = []

    for user_word in user_tokens:
        max_similarity = 0  # Initialize max similarity for the current user word

        for answer_word in answer_tokens:
            similarity = user_word.similarity(answer_word)
            if similarity > max_similarity:
                max_similarity = similarity

        word_similarities.append(max_similarity)

    if word_similarities:
        average_similarity = sum(word_similarities) / len(word_similarities)
        return average_similarity
    else:
        return 0

if __name__ == "__main__":
    main()
    # clean_csv("n5.csv")
