import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

# ===================== CONFIG =====================
API_URL = "https://nodered.mutambac.publicvm.com/api/data"
REFRESH_MS = 2000  # rafraîchissement toutes les 2 secondes

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="ESP32 Smart Dashboard",
    page_icon="",
    layout="centered"
)

# ===================== AUTO REFRESH =====================
st_autorefresh(interval=REFRESH_MS, key="refresh")

# ===================== TITRE =====================
st.title(" ESP32 Smart Dashboard")
st.caption("Données temps réel via MQTT → Node-RED → Streamlit Cloud")

# ===================== LECTURE API =====================
try:
    response = requests.get(API_URL, timeout=3)
    data = response.json()
except Exception as e:
    st.error(" Impossible de récupérer les données")
    st.stop()

# ===================== EXTRACTION DONNÉES =====================
temperature = data.get("temperature", "--")
humidity    = data.get("humidity", "--")
luminosity  = data.get("luminosity", "--")
sound       = data.get("sound", "--")

# ===================== AFFICHAGE =====================
col1, col2 = st.columns(2)
with col1:
    st.metric(" Température (°C)", temperature)
    st.metric(" Luminosité", luminosity)

with col2:
    st.metric(" Humidité (%)", humidity)
    st.metric(" Son", sound)

# ===================== DEBUG (OPTIONNEL) =====================
with st.expander(" Données brutes"):
    st.json(data)
