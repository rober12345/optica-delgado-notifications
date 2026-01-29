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
GUPSHUP_SOURCE = os.getenv("GUPSHUP_SOURCE")  # WhatsApp app name
TEMPLATE_NAME = os.getenv("GUPSHUP_TEMPLATE")

if not all([GUPSHUP_API_KEY, GUPSHUP_SOURCE, TEMPLATE_NAME]):
    st.error("Gupshup credentials are not configured.")
    st.stop()

# ---------------- FORM ----------------
with st.form("whatsapp_form"):
    pedido = st.text_input("Número de Pedido")
    telefono = st.text_input(
        "Número de WhatsApp del Cliente",
        placeholder="521234567890"
    )

    st.info(
        "Mensaje que recibirá el cliente:\n\n"
        f"Tu pedido {pedido or 'XXX'} ya está listo.\n"
        "Puedes pasar a Óptica Delgado por tus lentes."
    )

    enviar = st.form_submit_button("📤 Enviar WhatsApp")

# ---------------- SEND MESSAGE ----------------
if enviar:
    if not pedido or not telefono:
        st.warning("Por favor complete todos los campos.")
    else:
        payload = {
            "source": GUPSHUP_SOURCE,
            "destination": telefono,
            "template": f'{{"id":"{TEMPLATE_NAME}","params":["{pedido}"]}}'
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "apikey": GUPSHUP_API_KEY
        }

        try:
            response = requests.post(
                "https://api.gupshup.io/sm/api/v1/template/msg",
                data=payload,
                headers=headers,
                timeout=15
            )

            if response.status_code == 200:
                st.success("✅ WhatsApp enviado correctamente")
            else:
                st.error(f"❌ Error enviando WhatsApp: {response.text}")

        except Exception as e:
            st.error(f"🌐 Error de red: {e}")
