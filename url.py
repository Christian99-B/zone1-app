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

# Affichage des valeurs avec des couleurs et des rectangles
data = get_data()
if data:
    st.markdown("<h2 style='text-align: center; color: #3E4E60;'>Affichage des données en temps réel depuis l'ESP32</h2>", unsafe_allow_html=True)

    # Rectangle pour la température
    st.markdown(
        f"""
        <div style="background-color:#FF6347; padding:20px; margin:10px; border-radius:10px; color:white; font-size:24px; text-align:center;">
            Température (°C): {data['temperature']} °C
        </div>
        """, unsafe_allow_html=True)

    # Rectangle pour l'humidité
    st.markdown(
        f"""
        <div style="background-color:#4682B4; padding:20px; margin:10px; border-radius:10px; color:white; font-size:24px; text-align:center;">
            Humidité (%): {data['humidity']} %
        </div>
        """, unsafe_allow_html=True)

    # Rectangle pour le son
    st.markdown(
        f"""
        <div style="background-color:#32CD32; padding:20px; margin:10px; border-radius:10px; color:white; font-size:24px; text-align:center;">
            Son: {data['sound']}
        </div>
        """, unsafe_allow_html=True)

    # Rectangle pour la luminosité
    st.markdown(
        f"""
        <div style="background-color:#FFD700; padding:20px; margin:10px; border-radius:10px; color:white; font-size:24px; text-align:center;">
            Luminosité: {data['luminosity']}
        </div>
        """, unsafe_allow_html=True)

# Rafraîchissement manuel avec un bouton
if st.button('Rafraîchir les données'):
    st.experimental_rerun()
