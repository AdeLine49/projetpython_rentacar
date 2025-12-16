import streamlit as st
from core.car_rental_system import CarRentalSystem
from models.vehicle import Vehicle 

st.set_page_config(page_title="Gestion des Véhicules", page_icon="🚗")
st.title("🚗 Gestion des Véhicules")

# --- Constantes pour les choix de catégorie et d'état ---
VEHICLE_CATEGORIES = ["Voiture", "Camion", "Moto", "Bus"] 
VEHICLE_STATES = ["disponible", "loué", "en maintenance", "hors service"] 

# --- Initialisation du système de location ---
if "car_rental_system" not in st.session_state:
    st.session_state.car_rental_system = CarRentalSystem()
    # Ajout des véhicules initiaux avec les catégories et états cohérents.
   
    st.session_state.car_rental_system.add_vehicle("Renault", "Clio", "EF-456-GH", 40.0, "Voiture", "disponible")
    st.session_state.car_rental_system.add_vehicle("Peugeot", "308", "AB-123-CD", 55.0, "Voiture", "disponible")
    st.session_state.car_rental_system.add_vehicle("Mercedes", "Sprinter", "FG-789-HI", 90.0, "Camion", "disponible")
    st.session_state.car_rental_system.add_vehicle("Honda", "CB500F", "JK-456-LM", 30.0, "Moto", "en maintenance")
    st.session_state.car_rental_system.add_vehicle("Tesla", "Model 3", "TS-123-LA", 120.0, "Véhicule", "disponible")

# Récupérez l'instance du système de location depuis session_state
car_rental_system: CarRentalSystem = st.session_state.car_rental_system

menu = ["Ajouter un véhicule", "Afficher les véhicules", "Mettre à jour un véhicule", "Supprimer un véhicule"]
choice = st.sidebar.selectbox("Actions sur les véhicules", menu)

if choice == "Ajouter un véhicule":
    st.subheader("Ajouter un nouveau véhicule")
    with st.form("add_vehicle_form"):
        brand = st.text_input("Marque")
        model = st.text_input("Modèle")
        license_plate = st.text_input("Plaque d'immatriculation")
        daily_rate = st.number_input("Tarif journalier (€)", min_value=0.0, value=50.0)

        # Les index par défaut sont positionnés sur des valeurs courantes
        category = st.selectbox("Catégorie", options=VEHICLE_CATEGORIES, index=VEHICLE_CATEGORIES.index("Voiture")) 
        state = st.selectbox("État", options=VEHICLE_STATES, index=VEHICLE_STATES.index("disponible")) 

        submitted = st.form_submit_button("Ajouter le véhicule")
        if submitted:
            if brand and model and license_plate and daily_rate > 0 and category and state: 
                vehicle = car_rental_system.add_vehicle(brand, model, license_plate, daily_rate, category, state)
                if vehicle:
                    st.success(f"Véhicule {vehicle.brand} {vehicle.model} (ID: {vehicle.id}) ajouté avec succès.")
                    st.rerun()
                else:
                    st.error("Une erreur est survenue lors de l'ajout du véhicule. La plaque d'immatriculation existe peut-être déjà.")
            else:
                st.warning("Veuillez remplir tous les champs obligatoires et s'assurer que le tarif est positif.")

elif choice == "Afficher les véhicules":
    st.subheader("Liste de tous les véhicules")
    vehicles = car_rental_system.get_all_vehicles() 

    if vehicles:
        vehicle_data = []
        for v in vehicles:
            # L'attribut 'Disponible' est déduit de l'attribut 'state'
            est_disponible = "Oui" if v.state == "disponible" else "Non" 
            vehicle_data.append({
                "ID": v.id,
                "Marque": v.brand,
                "Modèle": v.model,
                "Plaque": v.license_plate,
                "Tarif/jour": f"{v.daily_rate:.2f}€",
                "Disponible": est_disponible, 
                "Catégorie": v.category,
                "État": v.state         
            })
        st.dataframe(vehicle_data, use_container_width=True)
    else:
        st.info("Aucun véhicule enregistré pour le moment.")

elif choice == "Mettre à jour un véhicule":
    st.subheader("Mettre à jour un véhicule existant")
    vehicles = car_rental_system.get_all_vehicles()
    if vehicles:
        vehicle_labels = {f"{v.brand} {v.model} ({v.license_plate}) - ID: {v.id}": v.id for v in vehicles}
        selected_vehicle_label = st.selectbox("Sélectionnez le véhicule à mettre à jour", list(vehicle_labels.keys()))

        if selected_vehicle_label:
            selected_vehicle_id = vehicle_labels[selected_vehicle_label]
            selected_vehicle = car_rental_system.find_vehicle(selected_vehicle_id)

            if selected_vehicle:
                with st.form("update_vehicle_form"):
                    new_brand = st.text_input("Nouvelle Marque", value=selected_vehicle.brand)
                    new_model = st.text_input("Nouveau Modèle", value=selected_vehicle.model)
                    new_license_plate = st.text_input("Nouvelle Plaque", value=selected_vehicle.license_plate)
                    new_daily_rate = st.number_input("Nouveau Tarif journalier (€)", min_value=0.0, value=selected_vehicle.daily_rate)
                    
                    # Logique pour la catégorie : gère l'erreur si la catégorie actuelle n'est pas dans la liste VEHICLE_CATEGORIES
                    current_category_index = VEHICLE_CATEGORIES.index(selected_vehicle.category) if selected_vehicle.category in VEHICLE_CATEGORIES else 0
                    new_category = st.selectbox("Nouvelle Catégorie", options=VEHICLE_CATEGORIES, index=current_category_index)
                    
                    # Logique pour l'état : gère l'erreur si l'état actuel n'est pas dans la liste VEHICLE_STATES
                    # Mappe également 'available' (ancienne valeur) à 'disponible' et gère les états inconnus
                    effective_current_state = selected_vehicle.state
                    if effective_current_state == 'available': # Si l'état vient d'un ancien format anglais
                        effective_current_state = 'disponible'
                    elif effective_current_state not in VEHICLE_STATES: # Si l'état est inconnu (ex: "Très bon")
                        effective_current_state = VEHICLE_STATES[0] # Défaut au premier état de la liste (ex: 'disponible')

                    current_state_index = VEHICLE_STATES.index(effective_current_state)
                    new_state = st.selectbox("Nouvel État", options=VEHICLE_STATES, index=current_state_index)

                    # La checkbox "Est disponible" est maintenant un indicateur lié au selectbox d'état,
                    # et n'est pas directement modifiable pour éviter les incohérences.
                    st.checkbox("Est disponible", value=(new_state == "disponible"), disabled=True, help="Cet indicateur est lié à l'état de location sélectionné ci-dessus.")

                    update_submitted = st.form_submit_button("Mettre à jour le véhicule")
                    if update_submitted:
                        if new_brand and new_model and new_license_plate and new_daily_rate > 0:
                            selected_vehicle.brand = new_brand
                            selected_vehicle.model = new_model
                            selected_vehicle.license_plate = new_license_plate
                            selected_vehicle.daily_rate = new_daily_rate
                            selected_vehicle.category = new_category
                            
                            # C'est ici que nous mettons à jour l'état et déduisons l'attribut is_available
                            selected_vehicle.state = new_state
                            selected_vehicle.is_available = (new_state == "disponible") # is_available est synchronisé avec l'état

                            st.success(f"Véhicule ID {selected_vehicle_id} mis à jour avec succès.")
                            st.rerun()
                        else:
                            st.error("Veuillez remplir tous les champs correctement.")
            else:
                st.error("Véhicule non trouvé.")
    else:
        st.info("Aucun véhicule à mettre à jour pour le moment.")

elif choice == "Supprimer un véhicule":
    st.subheader("Supprimer un véhicule")
    vehicles = car_rental_system.get_all_vehicles()
    if vehicles:
        vehicle_labels = {f"{v.brand} {v.model} ({v.license_plate}) - ID: {v.id}": v.id for v in vehicles}
        selected_vehicle_label = st.selectbox("Sélectionnez le véhicule à supprimer", list(vehicle_labels.keys()))

        if selected_vehicle_label:
            selected_vehicle_id = vehicle_labels[selected_vehicle_label]
            if st.button("Confirmer la suppression"):
                try:
                    vehicle_id_for_removal = int(selected_vehicle_id)
                    if car_rental_system.remove_vehicle(vehicle_id_for_removal):
                        st.success(f"Véhicule ID {vehicle_id_for_removal} supprimé avec succès.") 
                        st.rerun() 
                    else:
                        st.error(f"Impossible de supprimer le véhicule ID {vehicle_id_for_removal}. Il est peut-être loué.")
                except ValueError:
                    st.error("Erreur de type : l'ID du véhicule doit être un nombre entier.")
    else:
        st.info("Aucun véhicule à supprimer pour le moment.")
