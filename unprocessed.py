import pandas as pd
from googletrans import Translator
from slugify import slugify
import os
import requests

# Define the input CSV file path
input_csv_file = 'english.csv'

# Define the chunk size
chunk_size = 10

# Initialize the translator
translator = Translator()

# Define the list of target languages
target_languages = ['fr', 'es', 'da', 'nl', 'de', 'it', 'pt']

# Create a directory for each language and save the translated CSV files
for lang in target_languages:
    # Create a directory for the current language if it doesn't exist
    output_dir = f'{lang}_output'
    os.makedirs(output_dir, exist_ok=True)

    # Check if the translation has already been done for this language
    translated_csv_file = f'{output_dir}/translated_{lang}.csv'
    print(lang)
    if os.path.exists(translated_csv_file):
        translated_df = pd.read_csv(translated_csv_file, delimiter=';')
        processed_indices = set(translated_df.index)
    else:
        processed_indices = set()

    # Read the source CSV file in chunks
    for chunk in pd.read_csv(input_csv_file, delimiter=';', chunksize=chunk_size):
        # Initialize an empty DataFrame to store the unprocessed rows
        unprocessed_chunk = pd.DataFrame()

        # Iterate through the chunk and translate if not already processed
        for idx, row in chunk.iterrows():
            if idx not in processed_indices:
                try:
                    # Translate the text
                    translated_title = translator.translate(row[0], src='en', dest=lang).text 
                    translated_text = translator.translate(row[1], src='en', dest=lang).text
                except requests.exceptions.RequestException as e:
                    print(f"Error translating text at index {idx}: {e}")
                    # Add the unprocessed row to the unprocessed_chunk DataFrame
                    unprocessed_chunk = unprocessed_chunk.append(row)
                    continue
                except TypeError as e:
                    print(f"Type error on {idx}: {e}")
                    # Add the unprocessed row to the unprocessed_chunk DataFrame
                    try:
                        unprocessed_chunk = unprocessed_chunk.append(row)
                    except AttributeError: pass    
                    continue
                except AttributeError as e:
                    print(f"Attribute error on {idx}: {e}")
                    # Add the unprocessed row to the unprocessed_chunk DataFrame
                    try:
                        unprocessed_chunk = unprocessed_chunk.append(row)
                    except AttributeError: pass    
                    continue
                

                # Add the translated text and slugified column to the DataFrame
                chunk.at[idx, f'title_{lang}'] = translated_title
                chunk.at[idx, f'translated_{lang}'] = translated_text
                chunk.at[idx, 'slugified'] = slugify(row[0])

                # Mark the index as processed
                processed_indices.add(idx)

        # Append the unprocessed rows to the same output CSV file
        if os.path.exists(translated_csv_file):
            try:
              chunk[[f'title_{lang}',f'translated_{lang}','slugified']].to_csv(translated_csv_file, mode='a', header=False, index=False, sep=';')
            except KeyError: pass  
        else:
            try:
                chunk[[f'title_{lang}',f'translated_{lang}','slugified']].to_csv(translated_csv_file, index=False, sep=';')
            except: pass    

        # Save the unprocessed rows to a separate CSV file
        unprocessed_csv_file = f'{output_dir}/unprocessed_{lang}.csv'
        unprocessed_chunk.to_csv(unprocessed_csv_file, index=False, sep=';')

print("Translation and saving completed.")
