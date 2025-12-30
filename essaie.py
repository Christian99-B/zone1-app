import streamlit as st
import json
import time
import threading
import paho.mqtt.client as mqtt

# ================= CONFIG =================
MQTT_BROKER = "40.89.144.50"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/node1/data"

# ================= STREAMLIT =================
st.set_page_config(
    page_title="ESP32 MQTT Dashboard",
    layout="centered"
)

st.title("📡 ESP32 Smart Dashboard (MQTT)")
st.caption("Lecture via MQTT – compatible Streamlit Cloud")

# ================= SESSION STATE =================
if "data" not in st.session_state:
    st.session_state.data = None

# ================= MQTT CALLBACK =================
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        st.session_state.data = payload
    except Exception as e:
        print("Erreur JSON :", e)

def mqtt_thread():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC)
    client.loop_forever()

# ================= LANCEMENT MQTT =================
if "mqtt_started" not in st.session_state:
    threading.Thread(target=mqtt_thread, daemon=True).start()
    st.session_state.mqtt_started = True

# ================= AFFICHAGE =================
placeholder = st.empty()

while True:
    with placeholder.container():
        if st.session_state.data is None:
            st.warning("⏳ En attente des données MQTT...")
        else:
            d = st.session_state.data

            col1, col2 = st.columns(2)
            col3, col4 = st.columns(2)

            col1.metric("🌡 Température (°C)", d["temperature"])
            col2.metric("💧 Humidité (%)", d["humidity"])
            col3.metric("💡 Luminosité", d["luminosity"])
            col4.metric("🔊 Son", d["sound"])

            st.caption("📡 Données reçues via MQTT")

    time.sleep(2)
