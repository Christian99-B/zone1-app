import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# ===================== CONFIG =====================
API_DATA_URL = "https://nodered.mutambac.publicvm.com/api/data"
API_CMD_URL  = "https://nodered.mutambac.publicvm.com/api/node2/data"
REFRESH_MS = 2000

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="ESP32 Smart Dashboard",
    page_icon="📡",
    layout="wide"
)

# ===================== AUTO REFRESH =====================
st_autorefresh(interval=REFRESH_MS, key="refresh")

# ===================== TITRE =====================
st.markdown("""
# 📡 ESP32 Smart Dashboard  
**Supervision & Commande via MQTT / Node-RED**
""")

# ===================== LECTURE API =====================
try:
    response = requests.get(API_DATA_URL, timeout=3)
    data = response.json()
except:
    st.error("❌ Impossible de récupérer les données Node-RED")
    st.stop()

# ===================== EXTRACTION =====================
temperature = float(data.get("temperature", 0))
humidity    = float(data.get("humidity", 0))
luminosity  = int(data.get("luminosity", 0))
sound       = int(data.get("sound", 0))
timestamp   = datetime.now()

# ===================== METRICS =====================
c1, c2, c3, c4 = st.columns(4)
c1.metric("🌡 Température (°C)", f"{temperature:.1f}")
c2.metric("💧 Humidité (%)", f"{humidity:.1f}")
c3.metric("💡 Luminosité", luminosity)
c4.metric("🔊 Son", sound)

st.divider()

# ===================== HISTORIQUE =====================
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=["Time", "Température", "Humidité", "Luminosité", "Son"]
    )

# Ajouter nouvelle ligne
new_row = {
    "Time": timestamp,
    "Température": temperature,
    "Humidité": humidity,
    "Luminosité": luminosity,
    "Son": sound
}
st.session_state.history = pd.concat(
    [st.session_state.history, pd.DataFrame([new_row])],
    ignore_index=True
).tail(30)  # garder les 30 derniers points

df = st.session_state.history.set_index("Time")

# ===================== GRAPHIQUES =====================
st.subheader("📈 Évolution des capteurs")

colg1, colg2 = st.columns(2)

with colg1:
    st.markdown("### 🌡 Température / 💧 Humidité")
    st.line_chart(df[["Température", "Humidité"]])

with colg2:
    st.markdown("### 💡 Luminosité / 🔊 Son")
    st.area_chart(df[["Luminosité", "Son"]])

st.divider()

# ===================== COMMANDES =====================
st.subheader("🎛 Commande LED ESP32 #2 (GPIO15)")

col_led1, col_led2 = st.columns(2)

with col_led1:
    if st.button("💡 LED ON"):
        payload = {"led": True}
        try:
            requests.post(API_CMD_URL, json=payload, timeout=3)
            st.success("LED ESP32 #2 ALLUMÉE")
        except:
            st.error("Erreur envoi commande LED")

with col_led2:
    if st.button("⚫ LED OFF"):
        payload = {"led": False}
        try:
            requests.post(API_CMD_URL, json=payload, timeout=3)
            st.success("LED ESP32 #2 ÉTEINTE")
        except:
            st.error("Erreur envoi commande LED")

st.divider()

# ===================== DEBUG =====================
with st.expander("🛠 Données brutes (debug)"):
    st.json(data)
