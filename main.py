import streamlit as st
import requests
import os

st.set_page_config(page_title="Diagnóstico de Imagens com IA", layout="centered")

st.title("🧠 Diagnóstico por IA de Exames de Pulmão e Cérebro")
st.markdown("Envie uma imagem (raio-x, TC ou RM) e a IA irá analisar e descrever o que vê na imagem.")

tipo_exame = st.selectbox("Escolha o tipo de exame:", ["Pulmão", "Cérebro"])
imagem = st.file_uploader("📤 Envie a imagem do exame (JPG ou PNG)", type=["jpg", "jpeg", "png"])

API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

def analisar_imagem_na_replicate(imagem_bytes):
    url = "https://api.replicate.com/v1/predictions"
    headers = {
        "Authorization": f"Token {API_TOKEN}",
        "Content-Type": "application/json",
    }
    # Upload da imagem temporariamente no Replicate
    upload_url = "https://dreambooth-api-experimental.replicate.delivery/upload"
    resp = requests.post(upload_url, files={"file": imagem_bytes})
    image_url = resp.json()["url"]

    payload = {
        "version": "fc24cfc809edf0eb1ceba0c6033c49f3bbd240b99eae0cd1e909b1930c80a9a4",
        "input": {
            "image": image_url,
            "mode": "fast"
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    prediction = response.json()

    # Esperar até terminar
    prediction_url = prediction["urls"]["get"]
    status = prediction["status"]

    while status not in ["succeeded", "failed"]:
        result = requests.get(prediction_url, headers=headers).json()
        status = result["status"]
        if status == "succeeded":
            return result["output"]
        elif status == "failed":
            return "A análise falhou. Tente novamente."

    return "Erro ao processar a imagem."

if imagem is not None:
    st.image(imagem, caption="Imagem enviada", use_column_width=True)

    if st.button("🔍 Analisar com IA"):
        with st.spinner("A IA está analisando a imagem..."):
            resultado = analisar_imagem_na_replicate(imagem)
            st.subheader("🩺 Resultado da IA:")
            st.markdown(f"**Tipo de exame:** {tipo_exame}")
            st.markdown(f"**Diagnóstico e explicação:**\n\n{resultado}")
