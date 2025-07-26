import os
from alt_text_generator import generate_multilingual_alt_texts, save_to_airtable

# Set API keys and Airtable details
DEEPL_API_KEY = "f9c6f8ca-54ef-4dc2-8189-0254f547b9ec:fx"
AIRTABLE_API_KEY = "patOMNMSzIfDlNvx1.10a004d9f2c38a8acedeca455fb66c077c00532385eddb2151ab5ef308755bd4"
AIRTABLE_BASE_ID = "app6PZ4m7Lgt2poj9"
AIRTABLE_TABLE_NAME = "alt_data"

def batch_generate_from_folder(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(folder_path, file_name)
            result = generate_multilingual_alt_texts(image_path, DEEPL_API_KEY)
            save_to_airtable(result, AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
            print(f"Processed and saved: {file_name}")

if __name__ == "__main__":
    folder = "uploads"
    batch_generate_from_folder(folder)
