import streamlit as st
from core.car_rental_system import CarRentalSystem
import datetime

st.set_page_config(page_title="Locations en Cours", page_icon="📑")

st.title("📑 Locations en Cours")

# Assurez-vous que le système de location est bien initialisé dans session_state
if 'car_rental_system' not in st.session_state:
    st.session_state.car_rental_system = CarRentalSystem()

rental_system: CarRentalSystem = st.session_state.car_rental_system

current_rentals = rental_system.get_current_rentals()

if current_rentals:
    st.subheader("Liste des locations actives")

    # Préparer les données pour affichage
    rental_data = []
    for rental in current_rentals:
        # Convertir en int car find_customer attend un int, et customer.id est une string
        customer = rental_system.find_customer(int(rental.customer.id))
        # Convertir en int car find_vehicle attend un int, et vehicle.id est une string
        vehicle = rental_system.find_vehicle(int(rental.vehicle.id))

        customer_name = f"{customer.first_name} {customer.last_name}" if customer else "N/A"
        vehicle_info = f"{vehicle.brand} {vehicle.model} ({vehicle.license_plate})" if vehicle else "N/A"

        rental_data.append({
            "ID Location": rental.id, 
            "Client": customer_name,
            "Véhicule": vehicle_info,
            "Date Début": rental.start_date.strftime("%Y-%m-%d"),
            "Date Fin Prévue": rental.end_date.strftime("%Y-%m-%d"),
            "Coût Estimé": f"{rental.get_total_cost():.2f} €" 
        })

    st.dataframe(rental_data, use_container_width=True)

    st.subheader("Terminer une location")
    
    rentals_to_end_options = {}
    for r in current_rentals:
        # Assurez-vous que le client et le véhicule sont trouvés pour éviter des erreurs ici
        customer_for_display = rental_system.find_customer(int(r.customer.id))
        vehicle_for_display = rental_system.find_vehicle(int(r.vehicle.id))
        
        customer_name_display = customer_for_display.last_name if customer_for_display else "N/A"
        vehicle_plate_display = vehicle_for_display.license_plate if vehicle_for_display else "N/A"

        label = f"Location ID: {r.id} - Client: {customer_name_display} - Véhicule: {vehicle_plate_display}"
        rentals_to_end_options[label] = r.id


    if rentals_to_end_options:
        selected_rental_label = st.selectbox("Sélectionnez la location à terminer", list(rentals_to_end_options.keys()))
        selected_rental_id = rentals_to_end_options[selected_rental_label]

        return_date = st.date_input("Date de retour effective", datetime.date.today())

        if st.button("Terminer la location"):
            rental = rental_system.find_rental(selected_rental_id)
            if rental and rental.is_active: # is_active est une propriété, pas une méthode
                if return_date >= rental.start_date:
                    final_cost = rental_system.end_rental(selected_rental_id, return_date)
                    if final_cost is not None:
                        st.success(f"Location ID {selected_rental_id} terminée. Coût final : {final_cost:.2f} €")
                        st.rerun()
                    else:
                        st.error("Erreur lors de la terminaison de la location.")
                else:
                    st.error("La date de retour effective ne peut pas être antérieure à la date de début de location.")
            else:
                st.error("Location non trouvée ou déjà terminée.")
    else:
        st.info("Aucune location à terminer.")

else:
    st.info("Aucune location en cours pour le moment.")
