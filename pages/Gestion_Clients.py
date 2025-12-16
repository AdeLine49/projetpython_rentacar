import streamlit as st
from core.car_rental_system import CarRentalSystem
from models.customer import Customer # Importation nécessaire si vous manipulez directement des objets Customer

# Supprimez cette ligne ou celle qui suit si elle est en double
st.set_page_config(page_title="Gestion des Clients", page_icon="👥")
# Supprimez cette ligne ou celle qui suit si elle est en double
st.title("👥 Gestion des Clients")

# --- Initialisation du système de location (indispensable) ---
if "car_rental_system" not in st.session_state:
    st.session_state.car_rental_system = CarRentalSystem()
    # Optionnel : Ajoutez quelques clients pour la démonstration si l'app démarre ici
    st.session_state.car_rental_system.add_customer("Alice", "Dupont", 28, "AD12345","alicedupont@gmail.com")
    st.session_state.car_rental_system.add_customer("Bob", "Martin", 35, "BM67890", "bobmartin@gmail.com")

# Récupérez l'instance du système de location depuis session_state
car_rental_system: CarRentalSystem = st.session_state.car_rental_system

menu = ["Ajouter un client", "Afficher les clients", "Mettre à jour un client", "Supprimer un client"]
choice = st.sidebar.selectbox("Actions sur les clients", menu)

# Utilisez l'instance déjà définie au début du script
rental_system = car_rental_system # Assurez-vous d'utiliser une seule et même instance partout


if choice == "Ajouter un client":
    st.subheader("Ajouter un nouveau client")
    with st.form("add_customer_form"):
        first_name = st.text_input("Prénom")
        last_name = st.text_input("Nom de famille")
        email = st.text_input("Email")
        age = st.number_input("Âge", min_value=18, max_value=120, value=25)
        driver_license_number = st.text_input("Numéro de permis de conduire")

        submitted = st.form_submit_button("Ajouter le client")
        if submitted:
            if first_name and last_name and email and age and driver_license_number:
                customer = rental_system.add_customer(first_name, last_name, age, driver_license_number, email)
                if customer:
                    st.success(f"Client {customer.first_name} {customer.last_name} (ID: {customer.id}) ajouté avec succès.")
                    st.rerun()
                else:
                    st.error("Une erreur est survenue lors de l'ajout du client.")
            else:
                st.warning("Veuillez remplir tous les champs obligatoires.")

elif choice == "Afficher les clients":
    st.subheader("Liste de tous les clients")
    customers = car_rental_system.get_all_customers()
    if customers:
        customer_data = []
        for c in customers:
            history_summary = f"{len(c.rentals_history)} locations"

            customer_data.append({
                "ID": c.id,
                "Prénom": c.first_name,
                "Nom": c.last_name,
                "Email": c.email,
                "Âge": c.age,
                "Permis de Conduire": c.driver_license_number,
                "Historique des Locations": history_summary
            })
        st.dataframe(customer_data, use_container_width=True)
    else:
        st.info("Aucun client enregistré pour le moment.")

elif choice == "Mettre à jour un client":
    st.subheader("Mettre à jour un client existant")
    customers = car_rental_system.get_all_customers()
    if customers:
        customer_labels = {f"{c.first_name} {c.last_name} ({c.email}) - ID: {c.id}": c.id for c in customers}
        selected_customer_label = st.selectbox("Sélectionnez le client à mettre à jour", list(customer_labels.keys()))

        if selected_customer_label:
            selected_customer_id = customer_labels[selected_customer_label]
            selected_customer = car_rental_system.find_customer(selected_customer_id)

            if selected_customer:
                with st.form("update_customer_form"):
                    new_first_name = st.text_input("Nouveau Prénom", value=selected_customer.first_name)
                    new_last_name = st.text_input("Nouveau Nom", value=selected_customer.last_name)
                    new_email = st.text_input("Nouvel Email", value=selected_customer.email)
                    new_age = st.number_input("Nouvel Âge", value=selected_customer.age, min_value=18, max_value=120)
                    new_driver_license_number = st.text_input("Nouveau Numéro de Permis", value=selected_customer.driver_license_number)

                    update_submitted = st.form_submit_button("Mettre à jour")
                    if update_submitted:
                        if new_first_name and new_last_name and new_email:
                            selected_customer.first_name = new_first_name
                            selected_customer.last_name = new_last_name
                            selected_customer.email = new_email
                            selected_customer.age = new_age
                            selected_customer.driver_license_number = new_driver_license_number
                            st.success(f"Client ID {selected_customer_id} mis à jour.")
                            st.rerun()
                        else:
                            st.error("Veuillez remplir tous les champs correctement.")
            else:
                st.error("Client non trouvé.")
    else:
        st.info("Aucun client à mettre à jour.")

# Correction pour la suppression d'un client
elif choice == "Supprimer un client":
    st.subheader("Supprimer un client")
    customers = car_rental_system.get_all_customers()
    if customers:
        customer_labels = {f"{c.first_name} {c.last_name} ({c.email}) - ID: {c.id}": c.id for c in customers}
        selected_customer_label = st.selectbox("Sélectionnez le client à supprimer", list(customer_labels.keys()))

        if selected_customer_label:
            selected_customer_id = customer_labels[selected_customer_label]
            if st.button("Confirmer la suppression"):
                # >> C'EST ICI QU'IL FAUT AJOUTER LA CONVERSION EXPLICITE <<
                try:
                    customer_id_for_removal = int(selected_customer_id) # S'assurer que c'est un entier
                    if car_rental_system.remove_customer(customer_id_for_removal):
                        st.success(f"Client ID {customer_id_for_removal} supprimé avec succès.")
                        st.rerun()
                    else:
                        st.error("Impossible de supprimer le client. Vérifiez qu'il n'a pas de locations actives.")
                except ValueError:
                    st.error("Erreur de type : l'ID du client doit être un nombre entier.")
    else:
        st.info("Aucun client à supprimer.")
