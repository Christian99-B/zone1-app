import streamlit as st
import requests
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
st.autorefresh(interval=REFRESH_MS, key="refresh")

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

# ===================== METRICS (Rectangles) =====================
st.subheader("📊 Données des capteurs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="background-color:#f0f0f5;padding:10px;border-radius:10px;">
        <h4>Température (°C)</h4>
        <h3>{temperature:.1f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color:#f0f0f5;padding:10px;border-radius:10px;">
        <h4>Humidité (%)</h4>
        <h3>{humidity:.1f}</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background-color:#f0f0f5;padding:10px;border-radius:10px;">
        <h4>Luminosité</h4>
        <h3>{luminosity}</h3>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background-color:#f0f0f5;padding:10px;border-radius:10px;">
        <h4>Son</h4>
        <h3>{sound}</h3>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ===================== COMMANDES =====================
st.subheader("🎛 Commande LED ESP32 #2 (RGB)")

col_led1, col_led2, col_led3 = st.columns(3)

with col_led1:
    if st.button("💡 LED ROUGE ON"):
        payload = {"rgb": {"r": 255, "g": 0, "b": 0}}
        try:
            requests.post(API_CMD_URL, json=payload, timeout=3)
            st.success("LED ROUGE allumée")
        except:
            st.error("Erreur envoi commande LED")

with col_led2:
    if st.button("💡 LED VERTE ON"):
        payload = {"rgb": {"r": 0, "g": 255, "b": 0}}
        try:
            requests.post(API_CMD_URL, json=payload, timeout=3)
            st.success("LED VERTE allumée")
        except:
            st.error("Erreur envoi commande LED")

with col_led3:
    if st.button("💡 LED BLEUE ON"):
        payload = {"rgb": {"r": 0, "g": 0, "b": 255}}
        try:
            requests.post(API_CMD_URL, json=payload, timeout=3)
            st.success("LED BLEUE allumée")
        except:
            st.error("Erreur envoi commande LED")

st.divider()

# ===================== COMMANDES LED OFF =====================

col_led1_off, col_led2_off, col_led3_off = st.columns(3)

with col_led1_off:
    if st.button("⚫ LED ROUGE OFF"):
        payload = {"rgb": {"r": 0, "g": 0, "b": 0}}
        try:
            requests.post(API_CMD_URL, json=payload, timeout=3)
            st.success("LED ROUGE éteinte")
        except:
            st.error("Erreur envoi commande LED")

with col_led2_off:
    if st.button("⚫ LED VERTE OFF"):
        payload = {"rgb": {"r": 0, "g": 0, "b": 0}}
        try:
            requests.post(API_CMD_URL, json=payload, timeout=3)
            st.success("LED VERTE éteinte")
        except:
            st.error("Erreur envoi commande LED")

with col_led3_off:
    if st.button("⚫ LED BLEUE OFF"):
        payload = {"rgb": {"r": 0, "g": 0, "b": 0}}
        try:
            requests.post(API_CMD_URL, json=payload, timeout=3)
            st.success("LED BLEUE éteinte")
        except:
            st.error("Erreur envoi commande LED")

st.divider()

# ===================== DEBUG =====================
with st.expander("🛠 Données brutes (debug)"):
    st.json(data)

