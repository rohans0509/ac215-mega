# src/constants.py

gcp_project = "ac215-441200"
bucket_name = "ac215-mega-pipeline"

# Directory names as constants
SECRETS_DIR = "data/secrets"
INPUT_AUDIOS_DIR = "data/input_audios"
TEXT_PROMPTS_DIR = "data/text_prompts"
TEXT_PARAGRAPHS_DIR = "data/text_paragraphs"
TEXT_TRANSLATED_DIR = "data/text_translated"
OUTPUT_AUDIOS_DIR = "data/output_audios"

group_name = "group"  # Update this with your group name, e.g., "group-01"
assert group_name != "", "Update group name"
assert group_name != "pavlos-advanced", "Update group name"
