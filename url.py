import streamlit as st
import requests

# URL de l'API Node-RED pour contrôler les LED RGB (sans la LED rouge)
url_rgb_green_on = "https://nodered.mutambac.publicvm.com/api/rgb_green_on"
url_rgb_green_off = "https://nodered.mutambac.publicvm.com/api/rgb_green_off"
url_rgb_blue_on = "https://nodered.mutambac.publicvm.com/api/rgb_blue_on"
url_rgb_blue_off = "https://nodered.mutambac.publicvm.com/api/rgb_blue_off"

# Fonction pour envoyer les commandes aux LED RGB
def control_rgb(led_color, command):
    try:
        if led_color == "green":
            url_on = url_rgb_green_on if command == "on" else url_rgb_green_off
        elif led_color == "blue":
            url_on = url_rgb_blue_on if command == "on" else url_rgb_blue_off
        else:
            return

        response = requests.post(url_on)
        response.raise_for_status()
        return response.json()  # Vous pouvez traiter la réponse si nécessaire
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors du contrôle de la LED {led_color} : {e}")
        return None

# URL de l'API Node-RED pour récupérer les données des capteurs
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

# Personnaliser la couleur de l'interface
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f9; /* Couleur de fond générale */
        color: #333; /* Couleur du texte */
    }
    .css-1lcbv6s {
        background-color: #005792; /* Couleur du fond du titre */
        color: white; /* Couleur du texte */
    }
    </style>
    """, unsafe_allow_html=True)

# Affichage des valeurs avec des couleurs et des rectangles
data = get_data()
if data:
    st.markdown("<h2 style='text-align: center; color: #3E4E60;'>Affichage des données en temps réel depuis l'ESP32</h2>", unsafe_allow_html=True)

    # Rectangle pour la température
    st.markdown(
        f"""
        <div style="background-color:#FF6347; padding:20px; margin:10px; border-radius:10px; color:white; font-size:26px; text-align:center;">
            Température (°C): {data['temperature']} °C
        </div>
        """, unsafe_allow_html=True)

    # Rectangle pour l'humidité
    st.markdown(
        f"""
        <div style="background-color:#4682B4; padding:20px; margin:10px; border-radius:10px; color:white; font-size:26px; text-align:center;">
            Humidité (%): {data['humidity']} %
        </div>
        """, unsafe_allow_html=True)

    # Rectangle pour le son
    st.markdown(
        f"""
        <div style="background-color:#32CD32; padding:20px; margin:10px; border-radius:10px; color:white; font-size:26px; text-align:center;">
            Son: {data['sound']}
        </div>
        """, unsafe_allow_html=True)

    # Rectangle pour la luminosité
    st.markdown(
        f"""
        <div style="background-color:#FFD700; padding:20px; margin:10px; border-radius:10px; color:white; font-size:26px; text-align:center;">
            Luminosité: {data['luminosity']}
        </div>
        """, unsafe_allow_html=True)

    # Commandes pour la LED Verte
    col1, col2 = st.columns(2)
    with col1:
        # Ajout d'un encadrement coloré pour le bouton "Allumer LED Verte"
        if st.button("Allumer LED Verte", key="green_on", help="Allumer la LED verte", use_container_width=True):
            control_rgb("green", "on")
            st.success("LED Verte allumée")
    with col2:
        # Ajout d'un encadrement coloré pour le bouton "Éteindre LED Verte"
        if st.button("Éteindre LED Verte", key="green_off", help="Éteindre la LED verte", use_container_width=True):
            control_rgb("green", "off")
            st.success("LED Verte éteinte")

    # Commandes pour la LED Bleue
    col3, col4 = st.columns(2)
    with col3:
        # Ajout d'un encadrement coloré pour le bouton "Allumer LED Bleue"
        if st.button("Allumer LED Bleue", key="blue_on", help="Allumer la LED bleue", use_container_width=True):
            control_rgb("blue", "on")
            st.success("LED Bleue allumée")
    with col4:
        # Ajout d'un encadrement coloré pour le bouton "Éteindre LED Bleue"
        if st.button("Éteindre LED Bleue", key="blue_off", help="Éteindre la LED bleue", use_container_width=True):
            control_rgb("blue", "off")
            st.success("LED Bleue éteinte")

# Rafraîchissement manuel avec un bouton
if st.button('Rafraîchir les données'):
    st.experimental_rerun()
