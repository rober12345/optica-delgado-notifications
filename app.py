import streamlit as st
import requests
import os
from dotenv import load_dotenv

# ---------------- LOAD ENV ----------------
load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Óptica Delgado – WhatsApp",
    layout="centered"
)

st.title("📲 Óptica Delgado – Pedido Listo")
st.divider()

# ---------------- GUPSHUP CONFIG ----------------
GUPSHUP_API_KEY = os.getenv("GUPSHUP_API_KEY")
GUPSHUP_SOURCE_NUMBER = os.getenv("GUPSHUP_SOURCE_NUMBER")
GUPSHUP_TEMPLATE = os.getenv("GUPSHUP_TEMPLATE")
GUPSHUP_APP_NAME = os.getenv("GUPSHUP_APP_NAME")

if not all([GUPSHUP_API_KEY, GUPSHUP_SOURCE_NUMBER, GUPSHUP_TEMPLATE, GUPSHUP_APP_NAME]):
    st.error("❌ Missing Gupshup environment variables. Check your .env file.")
    st.stop()

# ---------------- FORM ----------------
with st.form("whatsapp_form"):
    pedido = st.text_input("📦 Número de Pedido")
    telefono = st.text_input("📞 Número de WhatsApp del Cliente", placeholder="521XXXXXXXXXX")

    st.info(
        "📩 Mensaje que recibirá el cliente:\n\n"
        "Hola, espero te encuentres muy bien al recibir este mensaje.\n\n"
        f"Tu pedido {pedido or 'XXXX'} ya está listo.\n\n"
        "Por favor, puedes pasar a Óptica Delgado por tus lentes."
    )

    enviar = st.form_submit_button("📤 Enviar WhatsApp")

# ---------------- FUNCTION ----------------
def send_whatsapp(destination, pedido_text):

    payload = {
        "channel": "whatsapp",
        "source": GUPSHUP_SOURCE_NUMBER,
        "destination": destination,
        "src.name": GUPSHUP_APP_NAME,
        "template": f'{{"id":"{GUPSHUP_TEMPLATE}","params":["{pedido_text}"]}}'
    }

    headers = {
        "apikey": GUPSHUP_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        response = requests.post(
            "https://api.gupshup.io/wa/api/v1/template/msg",
            data=payload,
            headers=headers,
            timeout=15
        )

        if response.status_code in (200, 202):
            st.success("✅ WhatsApp enviado correctamente")
        else:
            st.error(f"❌ Error enviando WhatsApp: {response.status_code} | {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"🌐 Network error: {e}")

# ---------------- SEND LOGIC ----------------
if enviar:
    if not pedido or not telefono:
        st.warning("⚠️ Por favor complete todos los campos.")
    else:
        send_whatsapp(telefono, pedido)
