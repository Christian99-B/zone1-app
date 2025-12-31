import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from datetime import datetime

# ===================== CONFIG =====================
API_DATA_URL = "https://nodered.mutambac.publicvm.com/api/data"
API_CMD_URL  = "https://nodered.mutambac.publicvm.com/api/node2/cmd"
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
**MQTT → Node-RED → Streamlit Cloud**  
""")

# ===================== LECTURE API =====================
try:
    response = requests.get(API_DATA_URL, timeout=3)
    data = response.json()
except:
    st.error(" Impossible de récupérer les données Node-RED")
    st.stop()

# ===================== EXTRACTION =====================
temperature = data.get("temperature", 0)
humidity    = data.get("humidity", 0)
luminosity  = data.get("luminosity", 0)
sound       = data.get("sound", 0)
timestamp   = data.get("timestamp", datetime.now().isoformat())

# ===================== METRICS =====================
c1, c2, c3, c4 = st.columns(4)
c1.metric("🌡 Température (°C)", f"{temperature}")
c2.metric("💧 Humidité (%)", f"{humidity}")
c3.metric("💡 Luminosité", f"{luminosity}")
c4.metric("🔊 Son", f"{sound}")

st.divider()

# ===================== GRAPHIQUES =====================
st.subheader("📈 Historique temps réel")

df = pd.DataFrame({
    "Température": [temperature],
    "Humidité": [humidity],
    "Luminosité": [luminosity],
    "Son": [sound]
})

colg1, colg2 = st.columns(2)
with colg1:
    st.line_chart(df[["Température", "Humidité"]])

with colg2:
    st.bar_chart(df[["Luminosité", "Son"]])

st.divider()

# ===================== COMMANDES =====================
st.subheader("🎛 Commandes ESP32 (via Node-RED)")

col_cmd1, col_cmd2 = st.columns(2)

# ---- RGB ----
with col_cmd1:
    st.markdown("### LED RGB")
    color = st.color_picker("Choisir une couleur", "#FF0000")

    if st.button("🚀 Envoyer couleur"):
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)

        payload = {
            "rgb": {"r": r, "g": g, "b": b}
        }

        try:
            requests.post(API_CMD_URL, json=payload, timeout=3)
            st.success(f"Couleur envoyée → R:{r} G:{g} B:{b}")
        except:
            st.error("Erreur envoi couleur")

# ---- MODE NUIT ----
with col_cmd2:
    st.markdown("### 🌙 Mode Nuit")

    if st.button("🌙 Activer mode nuit"):
        payload = {"night": 1}
        requests.post(API_CMD_URL, json=payload)
        st.success("Mode nuit ACTIVÉ")

    if st.button("☀ Désactiver mode nuit"):
        payload = {"night": 0}
        requests.post(API_CMD_URL, json=payload)
        st.success("Mode nuit DÉSACTIVÉ")

st.divider()

# ===================== DEBUG =====================
with st.expander("🛠 Données brutes (debug)"):
    st.json(data)
