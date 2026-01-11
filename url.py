import streamlit as st
import requests

# Fonction pour récupérer les données depuis l'API
def get_data():
    try:
        response = requests.get('http://adresse_de_votre_serveur_node_red/api/data')  #  serveur Node-RED
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            st.error("Échec de la récupération des données !")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return None

# Configuration de la page Streamlit
st.set_page_config(page_title="Données des capteurs", layout="wide")

# Récupération des données
data = get_data()

if data:
    # Affichage des données dans Streamlit
    st.title("Données des Capteurs")

    st.subheader("Température")
    st.write(f"{data['temperature']} °C")

    st.subheader("Humidité")
    st.write(f"{data['humidity']} %")

    st.subheader("Luminosité")
    st.write(f"{data['luminosity']} (valeur brute)")

    st.subheader("Son")
    st.write(f"{data['sound']} (valeur brute)")

else:
    st.warning("Aucune donnée disponible pour le moment.")
