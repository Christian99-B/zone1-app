import streamlit as st
import requests
import time

# URL de l'API Node-RED
url = "https://nodered.mutambac.publicvm.com/api/data"

# Fonction pour obtenir les données depuis Node-RED
def get_data():
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Affichage du tableau de bord
st.title("Tableau de bord IoT")
st.write("Affichage des données en temps réel depuis l'ESP32")

# Créer des éléments pour afficher les données
temperature = st.empty()
humidity = st.empty()
sound = st.empty()
luminosity = st.empty()

# Rafraîchissement des données toutes les 5 secondes
while True:
    data = get_data()
    if data:
        temperature.metric("Température (°C)", f"{data['temperature']} °C")
        humidity.metric("Humidité (%)", f"{data['humidity']} %")
        sound.metric("Son", f"{data['sound']}")
        luminosity.metric("Luminosité", f"{data['luminosity']}")
    
    time.sleep(5)  # Rafraîchissement toutes les 5 secondes
