import streamlit as st
import requests
import matplotlib.pyplot as plt

# Fonction pour récupérer les données depuis l'API Node-RED
def get_data():
    try:
        url = 'http://votre_serveur_node_red/api/data'  # Remplacez par l'URL de votre API
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Erreur lors de la récupération des données (code {response.status_code})")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur de connexion : {e}")
        return None

# Configuration de la page Streamlit
st.set_page_config(page_title="Dashboard IoT", layout="wide")

# Personnalisation des couleurs
st.markdown(
    """
    <style>
    .main {background-color: #f0f2f6;}
    h1 {color: #2f4f4f;}
    h2 {color: #4682b4;}
    .stButton>button {background-color: #4682b4; color: white;}
    .stButton>button:hover {background-color: #5a8dca;}
    </style>
    """, unsafe_allow_html=True)

# Titre du dashboard
st.title("Dashboard IoT - Données des Capteurs")

# Récupérer les données
data = get_data()

if data:
    # Affichage des données sous forme de cards (secteurs avec des couleurs)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Température")
        st.markdown(f"<h3 style='color:#FF6347;'>{data['temperature']} °C</h3>", unsafe_allow_html=True)
    
    with col2:
        st.subheader("Humidité")
        st.markdown(f"<h3 style='color:#20B2AA;'>{data['humidity']} %</h3>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Luminosité")
        st.markdown(f"<h3 style='color:#FFD700;'>{data['luminosity']} (valeur brute)</h3>", unsafe_allow_html=True)
    
    with col4:
        st.subheader("Son")
        st.markdown(f"<h3 style='color:#8A2BE2;'>{data['sound']} (valeur brute)</h3>", unsafe_allow_html=True)

    # Ajout d'un graphique pour la visualisation des données
    st.markdown("### Graphique des données des capteurs")

    fig, ax = plt.subplots()
    sensors = ['Température', 'Humidité', 'Luminosité', 'Son']
    values = [data['temperature'], data['humidity'], data['luminosity'], data['sound']]

    ax.bar(sensors, values, color=['#FF6347', '#20B2AA', '#FFD700', '#8A2BE2'])
    ax.set_xlabel('Capteurs')
    ax.set_ylabel('Valeur')
    ax.set_title('Comparaison des données des capteurs')
    
    # Affichage du graphique dans Streamlit
    st.pyplot(fig)

else:
    st.warning("Aucune donnée disponible pour le moment.")
