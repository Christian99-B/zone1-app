import streamlit as st
import requests

# URL de l'API Node-RED pour contrôler les LED RGB
url_rgb_red_on = "https://nodered.mutambac.publicvm.com/api/rgb_red_on"
url_rgb_red_off = "https://nodered.mutambac.publicvm.com/api/rgb_red_off"
url_rgb_green_on = "https://nodered.mutambac.publicvm.com/api/rgb_green_on"
url_rgb_green_off = "https://nodered.mutambac.publicvm.com/api/rgb_green_off"
url_rgb_blue_on = "https://nodered.mutambac.publicvm.com/api/rgb_blue_on"
url_rgb_blue_off = "https://nodered.mutambac.publicvm.com/api/rgb_blue_off"

# Fonction pour envoyer les commandes aux LED RGB
def control_rgb(led_color, command):
    try:
        if led_color == "red":
            url_on = url_rgb_red_on if command == "on" else url_rgb_red_off
        elif led_color == "green":
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

    # Commandes pour la LED Rouge
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Allumer LED Rouge"):
            control_rgb("red", "on")
            st.success("LED Rouge allumée")
    with col2:
        if st.button("Éteindre LED Rouge"):
            control_rgb("red", "off")
            st.success("LED Rouge éteinte")

    # Commandes pour la LED Verte
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Allumer LED Verte"):
            control_rgb("green", "on")
            st.success("LED Verte allumée")
    with col4:
        if st.button("Éteindre LED Verte"):
            control_rgb("green", "off")
            st.success("LED Verte éteinte")

    # Commandes pour la LED Bleue
    col5, col6 = st.columns(2)
    with col5:
        if st.button("Allumer LED Bleue"):
            control_rgb("blue", "on")
            st.success("LED Bleue allumée")
    with col6:
        if st.button("Éteindre LED Bleue"):
            control_rgb("blue", "off")
            st.success("LED Bleue éteinte")

# Rafraîchissement manuel avec un bouton
if st.button('Rafraîchir les données'):
    st.experimental_rerun()
