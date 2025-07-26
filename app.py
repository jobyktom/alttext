from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil, os

from alt_text_generator import generate_multilingual_alt_texts, save_to_airtable

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set your API keys and Airtable details here:
DEEPL_API_KEY = "f9c6f8ca-54ef-4dc2-8189-0254f547b9ec:fx"
AIRTABLE_API_KEY = "patOMNMSzIfDlNvx1.10a004d9f2c38a8acedeca455fb66c077c00532385eddb2151ab5ef308755bd4"
AIRTABLE_BASE_ID = "app6PZ4m7Lgt2poj9"
AIRTABLE_TABLE_NAME = "alt_data"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    result = generate_multilingual_alt_texts(file_path, DEEPL_API_KEY)
    save_to_airtable(result, AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
    
    return {"filename": file.filename, "alt_texts": result["alt_texts"]}
