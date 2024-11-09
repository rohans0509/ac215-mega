# src/transcribe.py

import os
import io
import ffmpeg
from tempfile import TemporaryDirectory
from google.cloud import speech
from .constants import INPUT_AUDIOS_DIR, TEXT_PROMPTS_DIR, group_name
from .utils import makedirs

def transcribe_audio_files():
    print("Transcribing audio files")
    makedirs()

    # Initialize Speech client
    client = speech.SpeechClient()

    # Get the list of audio files
    audio_files = os.listdir(INPUT_AUDIOS_DIR)

    for audio_filename in audio_files:
        uuid = audio_filename.replace(".mp3", "")
        audio_path = os.path.join(INPUT_AUDIOS_DIR, audio_filename)
        text_file = os.path.join(TEXT_PROMPTS_DIR, group_name, f"{uuid}.txt")

        if os.path.exists(text_file):
            continue

        print(f"Transcribing: {audio_path}")
        with TemporaryDirectory() as audio_dir:
            flac_path = os.path.join(audio_dir, "audio.flac")
            stream = ffmpeg.input(audio_path)
            stream = ffmpeg.output(stream, flac_path)
            ffmpeg.run(stream, quiet=True)

            with io.open(flac_path, "rb") as audio_file:
                content = audio_file.read()

            # Transcribe
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(language_code="en-US")
            operation = client.long_running_recognize(config=config, audio=audio)
            response = operation.result(timeout=90)
            print("response:", response)
            text = ""
            if len(response.results) > 0:
                text = response.results[0].alternatives[0].transcript
                print(text)
            else:
                text = "Transcription failed."

            # Save the transcription
            with open(text_file, "w") as f:
                f.write(text)
