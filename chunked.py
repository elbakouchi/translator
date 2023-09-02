import pandas as pd
from googletrans import Translator
from slugify import slugify
import os

# Define the input CSV file path
input_csv_file = 'english.csv'

# Define the chunk size
chunk_size = 5

# Initialize the translator
translator = Translator()

# Define the list of target languages
target_languages = ['fr', 'es', 'da', 'nl', 'de', 'it', 'pt']

# Create a directory for each language and save the translated CSV files
for lang in target_languages:
    # Create a directory for the current language if it doesn't exist
    output_dir = f'{lang}_output'
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through the CSV file in chunks
    for chunk in pd.read_csv(input_csv_file, delimiter=';', chunksize=chunk_size):
        # Translate the chunk of data
        for lang in target_languages:
            chunk[f'title_{lang}'] = chunk.iloc[:, 0].apply(lambda text: translator.translate(text, src='en', dest=lang).text)
            chunk[f'translated_{lang}'] = chunk.iloc[:, 1].apply(lambda text: translator.translate(text, src='en', dest=lang).text)
        
        # Slugify the first column (English text)
        chunk['slugified'] = chunk.iloc[:, 0].apply(slugify)

        # Save the translated chunk to a CSV file with the ';' separator
        output_csv_file = f'{output_dir}/translated_{lang}.csv'
        chunk.to_csv(output_csv_file, index=False, sep=';')

print("Translation and saving completed.")
