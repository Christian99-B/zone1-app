import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# ===================== CONFIG =====================
API_DATA_URL = "https://nodered.mutambac.publicvm.com/api/data"
API_CMD_URL  = "https://nodered.mutambac.publicvm.com/api/node1/data"
REFRESH_MS = 2000

# ===================== PAGE =====================
st.set_page_config(
    page_title="ESP32 Smart Dashboard",
    page_icon=" ",
    layout="wide"
)

st_autorefresh(interval=REFRESH_MS, key="refresh")

st.title("📡 ESP32 Smart Dashboard")
st.caption("Supervision & Commande ESP32 via Node-RED / MQTT")

# ===================== LECTURE API =====================
try:
    response = requests.get(API_DATA_URL, timeout=3)
    data = response.json()
except:
    st.error("Impossible de récupérer les données")
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
).tail(60)

df = st.session_state.history.set_index("Time")

# ===================== GRAPHIQUES =====================
st.subheader("📈 Graphiques des capteurs")

g1, g2 = st.columns(2)
g3, g4 = st.columns(2)

with g1:
    st.markdown("### 🌡 Température")
    st.line_chart(df["Température"])

with g2:
    st.markdown("### 💧 Humidité")
    st.line_chart(df["Humidité"])

with g3:
    st.markdown("### 💡 Luminosité (LDR)")
    st.line_chart(df["Luminosité"])

with g4:
    st.markdown("### 🔊 Son")
    st.line_chart(df["Son"])

st.divider()

# ===================== COMMANDES =====================
st.subheader("🎛 Commandes ESP32")

c_led1, c_led2, c_led3, c_motor = st.columns(4)

# 🔴 LED ROUGE
with c_led1:
    if st.button("🔴 LED Rouge"):
        requests.post(API_CMD_URL, json={"rgb": {"r":255,"g":0,"b":0}})
        st.success("LED Rouge ON")

# 🟢 LED VERTE
with c_led2:
    if st.button("🟢 LED Verte"):
        requests.post(API_CMD_URL, json={"rgb": {"r":0,"g":255,"b":0}})
        st.success("LED Verte ON")

# 🔵 LED BLEUE
with c_led3:
    if st.button("🔵 LED Bleue"):
        requests.post(API_CMD_URL, json={"rgb": {"r":0,"g":0,"b":255}})
        st.success("LED Bleue ON")

# ⚙️ MOTEUR
with c_motor:
    if st.button("⚙️ MOTEUR ON / OFF"):
        requests.post(API_CMD_URL, json={"motor": 1})
        st.success("Commande moteur envoyée")

st.divider()

# ===================== DEBUG =====================
with st.expander("🛠 Données brutes (debug)"):
    st.json(data)
