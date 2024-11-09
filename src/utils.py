# src/utils.py

import os
import shutil
import glob
from google.cloud import storage
from .constants import (
    gcp_project,
    bucket_name,
    group_name,
    SECRETS_DIR,
    INPUT_AUDIOS_DIR,
    TEXT_PROMPTS_DIR,
    TEXT_PARAGRAPHS_DIR,
    TEXT_TRANSLATED_DIR,
    OUTPUT_AUDIOS_DIR,
)

def makedirs():
    os.makedirs(SECRETS_DIR, exist_ok=True)
    os.makedirs(INPUT_AUDIOS_DIR, exist_ok=True)
    os.makedirs(os.path.join(TEXT_PROMPTS_DIR, group_name), exist_ok=True)
    os.makedirs(os.path.join(TEXT_PARAGRAPHS_DIR, group_name), exist_ok=True)
    os.makedirs(os.path.join(TEXT_TRANSLATED_DIR, group_name), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_AUDIOS_DIR, group_name), exist_ok=True)

def download_from_bucket(prefix, local_dir):
    print(f"Downloading from bucket: {prefix}")
    shutil.rmtree(local_dir, ignore_errors=True)
    os.makedirs(local_dir, exist_ok=True)

    client = storage.Client(project=gcp_project)
    bucket = client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)

    for blob in blobs:
        if not blob.name.endswith("/"):
            local_path = os.path.join(local_dir, os.path.basename(blob.name))
            blob.download_to_filename(local_path)
            print(f"Downloaded {blob.name} to {local_path}")

def upload_to_bucket(local_files_pattern, destination_prefix):
    print(f"Uploading to bucket: {destination_prefix}")
    client = storage.Client(project=gcp_project)
    bucket = client.bucket(bucket_name)
    local_files = glob.glob(local_files_pattern)

    for local_file in local_files:
        filename = os.path.basename(local_file)
        destination_blob_name = os.path.join(destination_prefix, filename)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file)
        print(f"Uploaded {local_file} to {destination_blob_name}")
