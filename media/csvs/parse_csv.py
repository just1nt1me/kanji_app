import pandas as pd
import regex as re

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

    # Remove kanji, hiragana, and katakana characters from the 'meaning' column
    kanji_hiragana_katakana = r'[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}]'
    df['meaning'] = df['meaning'].apply(lambda x: re.sub(kanji_hiragana_katakana, '', x))

    # Remove standalone occurrences of "vt" or "vi" or "eg"
    standalone_vt_vi_eg = r'\b(vt|vi|eg)\b'
    df['meaning'] = df['meaning'].str.replace(standalone_vt_vi_eg, '', regex=True)
    df['meaning'] = df['meaning'].apply(lambda x: x.lower())

    mask = df['expression'].apply(lambda x: contains_kanji_or_hiragana(x))          # Apply the function and create a boolean mask
    df = df[mask]                                                                   # Filter the DataFrame to keep rows with kanji or a mix of kanji and hiragana
    df.to_csv(csv, index=False)                                               # output the cleaned csv to the original file

def main():
    for csv in csv_list:
        clean_csv(csv)


if __name__ == "__main__":
    main()
    # clean_csv("n5.csv")
