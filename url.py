import streamlit as st
import requests

# URL de l'API Node-RED pour contrôler les LED RGB
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
st.title("Travail final SE et INDUSTRIE 4.0 A304/A311", anchor="top")

# Personnaliser la couleur de l'interface et occuper toute la largeur de l'écran
st.markdown(
    """
    <style>
    body {
        background-color: #003366; /* Couleur de fond générale - bleu foncé */
        color: white; /* Couleur du texte */
        font-family: 'Arial', sans-serif; /* Police moderne */
        margin: 0;
        padding: 0;
    }
    .css-1lcbv6s {
        background-color: #002244; /* Couleur du fond du titre - bleu foncé */
        color: white; /* Couleur du texte */
    }
    h1 {
        font-size: 40px;
        text-align: center;
        margin-top: 20px;
    }
    h2 {
        font-size: 28px;
        color: #D1E8E2; /* Couleur claire pour le sous-titre */
        text-align: center;
    }
    .value-box {
        padding: 20px;
        margin: 20px;
        border-radius: 15px;
        color: white;
        font-size: 24px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Ombres */
    }
    .temp { background-color: #FF6347; }
    .humidity { background-color: #4682B4; }
    .sound { background-color: #32CD32; }
    .luminosity { background-color: #FFD700; }
    .button-container {
        text-align: center;
        margin-top: 20px;
    }
    /* Rectangle en arrière-plan mauve */
    .background-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: #8A2BE2; /* Couleur mauve */
        z-index: -1; /* Mettre ce rectangle en arrière-plan */
        padding: 20px;
        border-radius: 20px;
    }

    .stButton>button {
        background-color: #005792; /* Couleur du fond du bouton */
        color: white; /* Texte du bouton */
        font-size: 18px;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #003C57; /* Couleur du bouton au survol */
    }
    </style>
    """, unsafe_allow_html=True)

# Ajouter le rectangle en arrière-plan
st.markdown('<div class="background-container"></div>', unsafe_allow_html=True)

# Affichage des valeurs avec des couleurs et des rectangles
data = get_data()
if data:
    st.markdown("<h2>Affichage des données en temps réel depuis l'ESP32</h2>", unsafe_allow_html=True)

    # Rectangle pour la température
    st.markdown(f'<div class="value-box temp">Température (°C): {data["temperature"]} °C</div>', unsafe_allow_html=True)

    # Rectangle pour l'humidité
    st.markdown(f'<div class="value-box humidity">Humidité (%): {data["humidity"]} %</div>', unsafe_allow_html=True)

    # Rectangle pour le son
    st.markdown(f'<div class="value-box sound">Son: {data["sound"]}</div>', unsafe_allow_html=True)

    # Rectangle pour la luminosité
    st.markdown(f'<div class="value-box luminosity">Luminosité: {data["luminosity"]}</div>', unsafe_allow_html=True)

    # Commandes pour la LED Verte
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Allumer LED Verte"):
            control_rgb("green", "on")
            st.success("LED Verte allumée")
    with col2:
        if st.button("Éteindre LED Verte"):
            control_rgb("green", "off")
            st.success("LED Verte éteinte")

    # Commandes pour la LED Bleue
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Allumer LED Bleue"):
            control_rgb("blue", "on")
            st.success("LED Bleue allumée")
    with col4:
        if st.button("Éteindre LED Bleue"):
            control_rgb("blue", "off")
            st.success("LED Bleue éteinte")

# Rafraîchissement manuel avec un bouton
if st.button('Rafraîchir les données'):
    st.experimental_rerun()
