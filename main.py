from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
    <html>
        <head>
            <title>Diagnóstico de Imagem IA</title>
        </head>
        <body style='text-align:center; padding-top: 100px; font-family: Arial;'>
            <h1>Envie sua imagem</h1>
            <form action='/upload' enctype='multipart/form-data' method='post'>
                <input name='file' type='file' accept='image/*'/>
                <br/><br/>
                <input type='submit' value='Analisar Imagem'/>
            </form>
        </body>
    </html>
    """
    return content

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    simulated_diagnosis = "Possível pneumonia detectada na região inferior direita do pulmão."

    return {
        "filename": file.filename,
        "diagnóstico_simulado": simulated_diagnosis,
        "mensagem": "Esta é uma simulação. Em breve será integrado com IA real."
    }
