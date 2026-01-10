import streamlit as st
import requests

# Fonction pour obtenir les données de Node-RED
def get_data():
    url = "http://<node-red-ip>:<port>/api/data"  # URL de l'API Node-RED
    response = requests.get(url)
    return response.json()  # Suppose que Node-RED renvoie un JSON avec les données

# Affichage des données dans Streamlit
st.title("Mon Dashboard IoT")
data = get_data()

if data:
    st.write(f"Température: {data['temperature']} °C")
    st.write(f"Humidité: {data['humidity']} %")
    st.write(f"Luminosité: {data['luminosity']}")
    st.write(f"Son: {data['sound']}")

    # Ajout du slider pour la LED RGB en PWM
    rgb_slider = st.slider("Contrôle de la LED RGB", min_value=0, max_value=255, value=128)
    # Vous pouvez envoyer cette valeur à Node-RED pour ajuster la LED
    # Exemple pour envoyer à Node-RED via une requête HTTP
    payload = {'rgb_value': rgb_slider}
    requests.post("http://<node-red-ip>:<port>/path/to/led_control", json=payload)
