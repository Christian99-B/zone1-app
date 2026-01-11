import streamlit as st
import requests


# Fonction pour récupérer les données depuis l'API
def get_data():
    try:
        response = requests.get('https://nodered.mutambac.publicvm.com/api/data')  #  serveur Node-RED
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

# Fonction pour obtenir les données de Node-RED
def get_data():
    url = "https://nodered.mutambac.publicvm.com/api/data"  # URL de l'API Node-RED
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
