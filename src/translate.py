# src/translate.py

import os
import glob
from googletrans import Translator
from .constants import TEXT_PARAGRAPHS_DIR, TEXT_TRANSLATED_DIR, group_name
from .utils import makedirs

def translate_texts():
    print("Translating texts")
    makedirs()

    translator = Translator()

    # Get the list of text files
    text_files = glob.glob(os.path.join(TEXT_PARAGRAPHS_DIR, group_name, "*.txt"))

    for text_file in text_files:
        uuid = os.path.basename(text_file).replace(".txt", "")
        translated_file = os.path.join(TEXT_TRANSLATED_DIR, group_name, f"{uuid}.txt")

        if os.path.exists(translated_file):
            continue

        with open(text_file) as f:
            input_text = f.read()

        print(f"Translating text for {uuid}")
        result = translator.translate(input_text, src="en", dest="fr")

        # Save the translated text
        with open(translated_file, "w") as f:
            f.write(result.text)
