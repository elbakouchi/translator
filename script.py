import pandas as pd
from googletrans import Translator
from slugify import slugify
import os

# Define the input CSV file path
input_csv_file = 'english.csv' #'~/1minscript/projects/metadatas/src/main/resources/company-activities-english.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(input_csv_file, delimiter=";")

# Initialize the translator
translator = Translator()

# Define the list of target languages
target_languages = ['fr', 'es', 'da', 'nl', 'de', 'it', 'pt']

# Loop through each target language
for lang in target_languages:
    # Create a new column for the translated text in the current language
    df[f'title_{lang}'] = df.iloc[:, 0].apply(lambda text: translator.translate(text, src='en', dest=lang).text)
    df[f'translated_{lang}'] = df.iloc[:, 1].apply(lambda text: translator.translate(text, src='en', dest=lang).text)


print("Given Dataframe :\n", df)

# Create a directory for each language and save the translated CSV files
for lang in target_languages:
    # Slugify the first column (English text)
    df['slugified'] = df.iloc[:, 0].apply(slugify)

    # Create a directory for the current language if it doesn't exist
    output_dir = f'{lang}_output'
    os.makedirs(output_dir, exist_ok=True)

    # Save the translated DataFrame to a CSV file
    output_csv_file = f'{output_dir}/translated_{lang}.csv'
    subdf = df[[f'title_{lang}',f'translated_{lang}','slugified']]
    subdf.to_csv(output_csv_file, index=False, sep=";")

print("Translation and saving completed.")
