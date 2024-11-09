# src/synthesize.py

import os
import glob
from google.cloud import storage
from google.cloud import texttospeech
from .constants import (
    gcp_project,
    bucket_name,
    OUTPUT_AUDIOS_DIR,
    TEXT_TRANSLATED_DIR,
    group_name,
)
from .utils import makedirs

def synthesize_audio():
    print("Synthesizing audio")
    makedirs()

    language_code = "fr-FR"  # Language code for French
    voice_name = "fr-FR-Standard-C"  # Voice name (you can choose any available voice)
    voice_gender = texttospeech.SsmlVoiceGender.FEMALE  # Voice gender

    client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

    # Get the list of text files
    text_files = glob.glob(os.path.join(TEXT_TRANSLATED_DIR, group_name, "*.txt"))
    for text_file in text_files:
        uuid = os.path.basename(text_file).replace(".txt", "")
        audio_blob_name = f"{OUTPUT_AUDIOS_DIR}/{group_name}/{uuid}.mp3"
        output_gcs_uri = f"gs://{bucket_name}/{audio_blob_name}"

        # Check if audio file already exists in GCS
        storage_client = storage.Client(project=gcp_project)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(audio_blob_name)

        if blob.exists():
            print(f"Audio file {audio_blob_name} already exists in GCS. Skipping.")
            continue

        with open(text_file, "r") as f:
            input_text = f.read()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=input_text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=voice_gender,
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        parent = f"projects/{gcp_project}/locations/us-central1"

        # Build the request
        request = texttospeech.SynthesizeLongAudioRequest(
            parent=parent,
            input=synthesis_input,
            audio_config=audio_config,
            voice=voice,
            output_gcs_uri=output_gcs_uri,
        )

        # Perform the long-running synthesis request
        operation = client.synthesize_long_audio(request=request)
        print(f"Started long audio synthesis for {uuid}. This may take some time...")

        # Wait for the operation to complete
        try:
            result = operation.result(timeout=3600)  # Adjust timeout as needed
            print(f"Audio content written to {output_gcs_uri}")
        except Exception as e:
            print(f"Error synthesizing {uuid}: {e}")

    print("Synthesis complete.")
