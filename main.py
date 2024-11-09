# main.py

from src.utils import makedirs, download_from_bucket, upload_to_bucket
from src.transcribe import transcribe_audio_files
from src.generate import generate_paragraphs
from src.translate import translate_texts
from src.synthesize import synthesize_audio
from src.constants import (
    group_name,
    INPUT_AUDIOS_DIR,
    TEXT_PROMPTS_DIR,
    TEXT_PARAGRAPHS_DIR,
    TEXT_TRANSLATED_DIR,
    OUTPUT_AUDIOS_DIR,
)

def main():
    # Ensure directories exist
    makedirs()

    # Step 1: Download input audio files
    download_from_bucket(prefix=f"{INPUT_AUDIOS_DIR}/", local_dir=INPUT_AUDIOS_DIR)

    # Step 2: Transcribe audio files
    transcribe_audio_files()

    # Step 3: Upload transcriptions
    upload_to_bucket(
        local_files_pattern=f"{TEXT_PROMPTS_DIR}/{group_name}/*.txt",
        destination_prefix=f"{TEXT_PROMPTS_DIR}/{group_name}/"
    )

    # Step 4: Generate paragraphs
    generate_paragraphs()

    # Step 5: Upload generated paragraphs
    upload_to_bucket(
        local_files_pattern=f"{TEXT_PARAGRAPHS_DIR}/{group_name}/*.txt",
        destination_prefix=f"{TEXT_PARAGRAPHS_DIR}/{group_name}/"
    )

    # Step 6: Translate texts
    translate_texts()

    # Step 7: Upload translated texts
    upload_to_bucket(
        local_files_pattern=f"{TEXT_TRANSLATED_DIR}/{group_name}/*.txt",
        destination_prefix=f"{TEXT_TRANSLATED_DIR}/{group_name}/"
    )

    # Step 8: Synthesize audio (outputs directly to GCS)
    synthesize_audio()

    # No need to upload synthesized audio since it's saved directly to GCS

if __name__ == "__main__":
    main()
