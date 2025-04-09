import os
import shutil
import requests
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def main():
    return """
    <html>
        <head>
            <title>Diagnóstico de Imagem IA</title>
        </head>
        <body style='font-family:Arial;text-align:center;padding-top:50px;'>
            <h1>Selecione o tipo de exame</h1>
            <form action='/upload' enctype='multipart/form-data' method='post'>
                <label><input type='radio' name='tipo' value='pulmao' checked/> Pulmão</label>
                <label><input type='radio' name='tipo' value='cerebro'/> Cérebro</label><br/><br/>
                <input name='file' type='file' accept='image/*'/><br/><br/>
                <input type='submit' value='Analisar'/>
            </form>
        </body>
    </html>
    """

@app.post("/upload")
async def upload_image(tipo: str = Form(...), file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Aqui vamos simular o diagnóstico e depois substituir com chamada real à Replicate
    if tipo == "pulmao":
        simulated_response = "Detectado: Possível pneumonia intersticial na base direita."
    else:
        simulated_response = "Detectado: Sinais de AVC isquêmico em região parietal esquerda."

    return {
        "tipo_exame": tipo,
        "arquivo": file.filename,
        "diagnóstico_IA": simulated_response,
        "nota": "Essa é uma simulação. A integração com IA real da Replicate será feita em seguida."
    }
