import streamlit as st 
from core.car_rental_system import CarRentalSystem

# Initialisation du système de location de voitures dans la session Streamlit
# Ceci permet de maintenir l'état du système (véhicules, clients, locations)
# lorsque l'utilisateur navigue entre les pages.
if 'car_rental_system' not in st.session_state:
    st.session_state.car_rental_system = CarRentalSystem()
    st.session_state.car_rental_system.add_vehicle("Toyota", "Corolla", "AB-123-CD", 50.0,"Voiture","available")
    st.session_state.car_rental_system.add_vehicle("Renault", "Clio", "EF-456-GH", 40.0, "Voiture","available")
    st.session_state.car_rental_system.add_vehicle("Yamaha", "MT-07", "WF-002-LD", 40.0, "Moto","available")
    st.session_state.car_rental_system.add_customer("Alice", "Dupont", 28, "AD12345", "alice@example.com")
    st.session_state.car_rental_system.add_customer("Bob", "Martin", 22, "BM67890","charlie@exemple.com")


st.set_page_config(
    page_title="Système de Location de Voitures",
    page_icon="🚗",
    layout="wide" # ou "centered"
)

st.title("🚗 Bienvenue dans le Système de Location de Voitures")

st.markdown("""
Bienvenue dans l'application de gestion de location de voitures.
Utilisez la barre latérale pour naviguer entre les différentes sections :
- **Accueil** : Informations générales.
- **Gestion Véhicules** : Ajouter, afficher, modifier et supprimer des véhicules.
- **Gestion Clients** : Ajouter, afficher, modifier et supprimer des clients.
- **Nouvelle Location** : Enregistrer une nouvelle location.
- **Locations en cours** : Gérer et terminer les locations actives.
- **Rapports** : Consulter les véhicules disponibles, le chiffre d'affaires, etc.

---
""")

st.info("Sélectionnez une page dans le menu de gauche pour commencer.")




# ajout ici d'un petit résumé ou des statistiques globales si vous le souhaitez
rental_system = st.session_state.car_rental_system
st.subheader("Statistiques Rapides")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Véhicules enregistrés", len(rental_system.get_all_vehicles()))
with col2:
    st.metric("Clients enregistrés", len(rental_system.get_all_customers()))
with col3:
    st.metric("Locations en cours", len(rental_system.get_current_rentals()))