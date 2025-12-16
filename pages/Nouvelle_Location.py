import streamlit as st
import datetime
# Assurez-vous d'importer car_rental_system depuis le bon chemin si ce n'est pas déjà fait
from core.car_rental_system import CarRentalSystem

# Initialiser le système de location dans st.session_state si ce n'est pas déjà fait
if 'car_rental_system' not in st.session_state:
    st.session_state.car_rental_system = CarRentalSystem()
car_rental_system: CarRentalSystem = st.session_state.car_rental_system


st.title("Créer une nouvelle location")

# --- Formulaire de création de location ---

# Récupérer les clients pour le sélecteur
customers_for_select = {f"{c.first_name} {c.last_name} (ID: {c.id}, Âge: {c.age})": c.id for c in car_rental_system.customers.values()}
selected_customer_label = st.selectbox("Sélectionner un client", options=list(customers_for_select.keys()))
customer_id_input = customers_for_select.get(selected_customer_label)

# Récupérer les véhicules disponibles
available_vehicles = car_rental_system.get_available_vehicles()
vehicles_for_select = {f"{v.brand} {v.model} ({v.category}, Tarif: {v.daily_rate}€/jour)": v.id for v in available_vehicles}
selected_vehicle_label = st.selectbox("Sélectionner un véhicule disponible", options=list(vehicles_for_select.keys()))
vehicle_id_input = vehicles_for_select.get(selected_vehicle_label)

# Champs de date
start_date_input = st.date_input("Date de début", datetime.date.today())
end_date_input = st.date_input("Date de fin", datetime.date.today() + datetime.timedelta(days=1))


if st.button("Confirmer la location"):
    if customer_id_input is not None and vehicle_id_input is not None: # Vérifier que les IDs sont bien sélectionnés
        # Appeler la méthode create_rental modifiée
        # Nous nous attendons maintenant à un tuple (Rental ou None, Message d'erreur ou None)
        new_rental, error_message = car_rental_system.create_rental(
            customer_id_input, vehicle_id_input, start_date_input, end_date_input
        )

        if new_rental:
            st.success(f"Location {new_rental.id} de {new_rental.vehicle.brand} {new_rental.vehicle.model} pour {new_rental.customer.first_name} {new_rental.customer.last_name} créée avec succès!")
            st.rerun() # Rafraîchir pour mettre à jour les listes
        else:
            # Afficher l'erreur retournée par la fonction create_rental
            st.error(error_message)
    else:
        st.warning("Veuillez sélectionner un client et un véhicule.")

# Optionnel : Afficher la liste des locations existantes ou les véhicules disponibles après création
st.subheader("Locations Actuelles")
current_rentals = car_rental_system.get_current_rentals()
if current_rentals:
    for rental in current_rentals:
        st.write(f"ID: {rental.id}, Client: {rental.customer.first_name} {rental.customer.last_name}, Véhicule: {rental.vehicle.brand} {rental.vehicle.model}, Début: {rental.start_date}, Fin: {rental.end_date}")
else:
    st.info("Aucune location active pour le moment.")
