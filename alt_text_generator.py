from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import deepl
from pyairtable import Table

# Load BLIP once (singleton)
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def generate_caption(image_path):
    image = Image.open(image_path).convert('RGB')
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def translate_text(text, target_lang, api_key):
    translator = deepl.Translator(api_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text

def generate_multilingual_alt_texts(image_path, deepl_api_key):
    base_caption = generate_caption(image_path)
    languages = {
        "en": base_caption,
        "de": translate_text(base_caption, "DE", deepl_api_key),
        "es": translate_text(base_caption, "ES", deepl_api_key),
        "it": translate_text(base_caption, "IT", deepl_api_key),
        "fr": translate_text(base_caption, "FR", deepl_api_key),
        "nl": translate_text(base_caption, "NL", deepl_api_key),
    }
    return {
        "image": image_path.split("/")[-1],
        "alt_texts": languages
    }

def save_to_airtable(record, api_key, base_id, table_name):
    table = Table(api_key, base_id, table_name)
    fields = {
        "Image": record["image"],
        "Alt EN": record["alt_texts"]["en"],
        "Alt DE": record["alt_texts"]["de"],
        "Alt ES": record["alt_texts"]["es"],
        "Alt IT": record["alt_texts"]["it"],
        "Alt FR": record["alt_texts"]["fr"],
        "Alt NL": record["alt_texts"]["nl"],
    }
    table.create(fields)
