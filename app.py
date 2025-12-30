import streamlit as st
import requests
import time

# ================= CONFIG =================
ESP32_URL = "http://192.168.137.11/data"
REFRESH_SEC = 3

st.set_page_config(
    page_title="ESP32 Smart Dashboard",
    page_icon="📡",
    layout="centered"
)

# ================= STYLE CSS =================
st.markdown("""
<style>
body {
    background-color: #f5f7fa;
}

.card {
    padding: 20px;
    border-radius: 16px;
    color: white;
    text-align: center;
    font-size: 22px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
}

.temp { background: linear-gradient(135deg, #ff512f, #dd2476); }
.hum  { background: linear-gradient(135deg, #36d1dc, #5b86e5); }
.light{ background: linear-gradient(135deg, #f7971e, #ffd200); color: black; }
.sound{ background: linear-gradient(135deg, #8e2de2, #4a00e0); }

.title {
    font-size: 34px;
    font-weight: bold;
}

.subtitle {
    color: #6c757d;
}
</style>
""", unsafe_allow_html=True)

# ================= TITRE =================
st.markdown('<div class="title">📡 ESP32 Smart Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Lecture directe depuis l’ESP32 (sans Firebase)</div>', unsafe_allow_html=True)
st.markdown("---")

placeholder = st.empty()

# ================= LOOP =================
while True:
    try:
        r = requests.get(ESP32_URL, timeout=2)
        data = r.json()

        with placeholder.container():
            c1, c2 = st.columns(2)
            c3, c4 = st.columns(2)

            c1.markdown(
                f'<div class="card temp">🌡️ Température<br><b>{data["temperature"]:.1f} °C</b></div>',
                unsafe_allow_html=True
            )

            c2.markdown(
                f'<div class="card hum">💧 Humidité<br><b>{data["humidity"]:.1f} %</b></div>',
                unsafe_allow_html=True
            )

            c3.markdown(
                f'<div class="card light">💡 Luminosité<br><b>{data["luminosity"]}</b></div>',
                unsafe_allow_html=True
            )

            c4.markdown(
                f'<div class="card sound">🔊 Son<br><b>{data["sound"]}</b></div>',
                unsafe_allow_html=True
            )

            st.caption("🔄 Mise à jour automatique toutes les 3 secondes")

    except:
        st.error("❌ ESP32 non accessible")

    time.sleep(REFRESH_SEC)
