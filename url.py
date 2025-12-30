import streamlit as st
import requests
import time

API_URL = "https://nodered.mutambac.publicvm.com/api/data"
REFRESH = 3

st.set_page_config(
    page_title="ESP32 Smart Dashboard",
    layout="centered"
)

st.title("📡 ESP32 Smart Dashboard")
st.caption("Données temps réel via MQTT → Node-RED → Streamlit Cloud")

try:
    r = requests.get(API_URL, timeout=3)
    data = r.json()
except:
    st.error("Impossible de contacter Node-RED")
    st.stop()

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

col1.metric("🌡 Température (°C)", data["temperature"])
col2.metric("💧 Humidité (%)", data["humidity"])
col3.metric("💡 Luminosité", data["luminosity"])
col4.metric("🔊 Son", data["sound"])

time.sleep(REFRESH)
st.rerun()
