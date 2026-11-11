import streamlit as st
from db import create_tables

# Configuration de la page
st.set_page_config(
    page_title="Stage Tracker",
    page_icon="🎯",
    layout="wide"
)

# Initialisation de la base de données
create_tables()

# Titre principal
st.title("🎯 Stage Tracker")
st.write("Bienvenue dans ton gestionnaire de candidatures de stage !")

# Menu de navigation
page = st.sidebar.radio(
    "Navigation",
    ["Accueil", "Offres", "Candidatures", "Statistiques"]
)

if page == "Accueil":
    st.header("🏠 Tableau de bord")
    st.write("Bienvenue sur Stage Tracker !")

elif page == "Offres":
    st.header("💼 Offres de stage")
    st.write("Consulte et gère tes offres de stage.")

elif page == "Candidatures":
    st.header("📋 Mes candidatures")
    st.write("Suis l'évolution de tes candidatures.")

elif page == "Statistiques":
    st.header("📊 Statistiques")
    st.write("Analyse tes candidatures.")