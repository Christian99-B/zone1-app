import streamlit as st
import requests

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

# Appliquer du style au tableau de bord
st.title("Tableau de bord IoT", anchor="top")

# Affichage des valeurs avec des couleurs et des améliorations de style
data = get_data()
if data:
    st.markdown("<h2 style='text-align: center; color: #3E4E60;'>Affichage des données en temps réel depuis l'ESP32</h2>", unsafe_allow_html=True)

    # Utilisation des couleurs dans les metrics
    st.markdown('<p style="color:#5B9BD5; font-size:20px;">Température (°C)</p>', unsafe_allow_html=True)
    st.metric(label="Température", value=f"{data['temperature']} °C", delta=None, delta_color="normal", help="Température mesurée par le capteur DHT11")

    st.markdown('<p style="color:#5B9BD5; font-size:20px;">Humidité (%)</p>', unsafe_allow_html=True)
    st.metric(label="Humidité", value=f"{data['humidity']} %", delta=None, delta_color="normal", help="Humidité mesurée par le capteur DHT11")

    st.markdown('<p style="color:#5B9BD5; font-size:20px;">Son</p>', unsafe_allow_html=True)
    st.metric(label="Son", value=f"{data['sound']}", delta=None, delta_color="normal", help="Niveau sonore mesuré")

    st.markdown('<p style="color:#5B9BD5; font-size:20px;">Luminosité</p>', unsafe_allow_html=True)
    st.metric(label="Luminosité", value=f"{data['luminosity']}", delta=None, delta_color="normal", help="Luminosité mesurée par le capteur LDR")

# Rafraîchissement manuel avec un bouton
if st.button('Rafraîchir les données'):
    st.experimental_rerun()
