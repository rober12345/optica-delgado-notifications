import streamlit as st
import requests
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Óptica Delgado – WhatsApp",
    layout="centered"
)

st.title("📲 Óptica Delgado – Pedido Listo")
st.divider()

# ---------------- GUPSHUP CONFIG ----------------
GUPSHUP_API_KEY = os.getenv("GUPSHUP_API_KEY")
WHATSAPP_SOURCE_NUMBER = os.getenv("GUPSHUP_SOURCE_NUMBER")
TEMPLATE_NAME = os.getenv("GUPSHUP_TEMPLATE")

if not all([GUPSHUP_API_KEY, WHATSAPP_SOURCE_NUMBER, TEMPLATE_NAME]):
    st.error("❌ Gupshup environment variables are not configured.")
    st.stop()

# ---------------- FORM ----------------
with st.form("whatsapp_form"):
    pedido = st.text_input("📦 Número de Pedido")
    telefono = st.text_input(
        "📞 Número de WhatsApp del Cliente",
        placeholder="521XXXXXXXXXX"
    )

    st.info(
        "📩 Mensaje que recibirá el cliente:\n\n"
        "Hola, espero te encuentres muy bien al recibir este mensaje.\n\n"
        f"Tu pedido {pedido or 'XXXX'} ya está listo.\n\n"
        "Por favor, puedes pasar a Óptica Delgado por tus lentes."
    )

    enviar = st.form_submit_button("📤 Enviar WhatsApp")

# ---------------- SEND MESSAGE ----------------
if enviar:
    if not pedido or not telefono:
        st.warning("⚠️ Por favor complete todos los campos.")
    else:
        payload = {
            "channel": "whatsapp",
            "source": WHATSAPP_SOURCE_NUMBER,
            "destination": telefono,
            "message": {
                "type": "template",
                "template": {
                    "id": TEMPLATE_NAME,
                    "params": [pedido]
                }
            }
        }

        headers = {
            "apikey": GUPSHUP_API_KEY,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                "https://api.gupshup.io/wa/api/v1/template/msg",
                headers=headers,
                json=payload,
                timeout=15
            )

            if response.status_code in (200, 202):
                st.success("✅ WhatsApp enviado correctamente")
            else:
                st.error(f"❌ Error enviando WhatsApp: {response.text}")

        except Exception as e:
            st.error(f"🌐 Error de red: {e}")
