import streamlit as st
from core.car_rental_system import CarRentalSystem
import datetime # Importation utile pour les formats de date si nécessaire, bien que strftime soit suffisant

st.set_page_config(page_title="Rapports", page_icon="📈")

st.title("📈 Rapports")

if 'car_rental_system' not in st.session_state:
    st.session_state.car_rental_system = CarRentalSystem()

rental_system: CarRentalSystem = st.session_state.car_rental_system

report_type = st.sidebar.selectbox("Choisissez un type de rapport",
                                    ["Véhicules disponibles", "Locations en cours", "Chiffre d'affaires", "Statistiques"])

if report_type == "Véhicules disponibles":
    st.subheader("Véhicules disponibles")
    available_vehicles = rental_system.get_available_vehicles()
    if available_vehicles:
        data = [{"ID": v.id, "Marque": v.brand, "Modèle": v.model,
                 "Plaque": v.license_plate, "Tarif Journalier": f"{v.daily_rate:.2f} €"} for v in available_vehicles]
        st.dataframe(data, use_container_width=True)
    else:
        st.info("Tous les véhicules sont actuellement loués ou aucun véhicule n'est enregistré.")

elif report_type == "Locations en cours":
    st.subheader("Locations en cours")
    current_rentals = rental_system.get_current_rentals()
    if current_rentals:
        rental_data = []
        for rental in current_rentals:
            # Accéder à l'ID du client via l'objet customer embarqué dans rental
            # et le convertir en int pour la méthode find_customer si nécessaire.
            customer = rental_system.find_customer(int(rental.customer.id))
            # Accéder à l'ID du véhicule via l'objet vehicle embarqué dans rental
            # et le convertir en int pour la méthode find_vehicle si nécessaire.
            vehicle = rental_system.find_vehicle(int(rental.vehicle.id))

            customer_name = f"{customer.first_name} {customer.last_name}" if customer else "N/A"
            vehicle_info = f"{vehicle.brand} {vehicle.model} ({vehicle.license_plate})" if vehicle else "N/A"

            rental_data.append({
                "ID Location": rental.id, # CORRECTION 3: Utiliser rental.id
                "Client": customer_name,
                "Véhicule": vehicle_info,
                "Date Début": rental.start_date.strftime("%Y-%m-%d"),
                "Date Fin Prévue": rental.end_date.strftime("%Y-%m-%d"),
                "Coût Estimé": f"{rental.get_total_cost():.2f} €" 
            })
        st.dataframe(rental_data, use_container_width=True)
    else:
        st.info("Aucune location en cours.")

elif report_type == "Chiffre d'affaires":
    st.subheader("Chiffre d'affaires total")
    total_revenue = rental_system.calculate_total_revenue()
    st.success(f"Le chiffre d'affaires total à ce jour est de : **{total_revenue:.2f} €**")

    # Historique des locations terminées
    st.markdown("---")
    st.subheader("Détail des locations terminées")
    # is_active est une propriété, pas une méthode
    completed_rentals = [r for r in rental_system.get_all_rentals() if not r.is_active]
    if completed_rentals:
        rental_data = []
        for rental in completed_rentals:
            #  Accéder à l'ID du client via l'objet customer embarqué dans rental
            customer = rental_system.find_customer(int(rental.customer.id))
            #  Accéder à l'ID du véhicule via l'objet vehicle embarqué dans rental
            vehicle = rental_system.find_vehicle(int(rental.vehicle.id))

            customer_name = f"{customer.first_name} {customer.last_name}" if customer else "N/A"
            vehicle_info = f"{vehicle.brand} {vehicle.model} ({vehicle.license_plate})" if vehicle else "N/A"

            rental_data.append({
                "ID Location": rental.id, # CORRECTION 7: Utiliser rental.id
                "Client": customer_name,
                "Véhicule": vehicle_info,
                "Date Début": rental.start_date.strftime("%Y-%m-%d"),
                "Date Fin Prévue": rental.end_date.strftime("%Y-%m-%d"),
                "Date Retour Eff.": rental.actual_return_date.strftime("%Y-%m-%d") if rental.actual_return_date else "N/A", 
                "Coût Final": f"{rental.final_billed_amount:.2f} €" if rental.final_billed_amount is not None else "N/A" 
            })
        st.dataframe(rental_data, use_container_width=True)
    else:
        st.info("Aucune location terminée enregistrée.")

elif report_type == "Statistiques":
    st.subheader("Statistiques globales")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Véhicules", len(rental_system.get_all_vehicles()))
        st.metric("Total Clients", len(rental_system.get_all_customers()))
    with col2:
        st.metric("Locations Actives", len(rental_system.get_current_rentals()))
        st.metric("Locations Terminées", len([r for r in rental_system.get_all_rentals() if not r.is_active]))

    st.markdown("---")
    st.subheader("Disponibilité des véhicules")
    available_count = len(rental_system.get_available_vehicles())
    total_count = len(rental_system.get_all_vehicles())

    if total_count > 0:
        st.progress(available_count / total_count, text=f"{available_count} véhicules disponibles sur {total_count}")
    else:
        st.info("Aucun véhicule enregistré pour calculer la disponibilité.")
