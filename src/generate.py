# src/generate.py

import os
import glob
import vertexai
from vertexai.language_models import TextGenerationModel
from .constants import (
    TEXT_PROMPTS_DIR,
    TEXT_PARAGRAPHS_DIR,
    group_name,
    gcp_project,
)
from .utils import makedirs

def generate_paragraphs():
    print("Generating paragraphs")
    makedirs()

    vertexai.init(project=gcp_project, location="us-central1")
    model = TextGenerationModel.from_pretrained("text-bison@001")

    # Get the list of text files
    text_files = glob.glob(os.path.join(TEXT_PROMPTS_DIR, group_name, "*.txt"))

    for text_file in text_files:
        uuid = os.path.basename(text_file).replace(".txt", "")
        paragraph_file = os.path.join(TEXT_PARAGRAPHS_DIR, group_name, f"{uuid}.txt")

        if os.path.exists(paragraph_file):
            continue

        with open(text_file) as f:
            input_text = f.read()

        # Generate output
        input_prompt = f"""
        Create a transcript for a podcast about cheese with 1000 or more words.
        Use the text below as a starting point.
        Do not include speaker names or any extra formatting.
        The host's name is Pavlos Protopapas.
        {input_text}
        """

        print(f"Generating text for {uuid}")
        response = model.predict(input_prompt, max_output_tokens=1024, temperature=0.5)
        paragraph = response.text

        # Save the generated paragraph
        with open(paragraph_file, "w") as f:
            f.write(paragraph)
