import datetime
from typing import List, Dict, Optional, Tuple
from models.vehicle import Vehicle, Car, Truck, Motorcycle
from models.customer import Customer
from models.rental import Rental

class CarRentalSystem:
    
    #Classe centrale pour gérer le système de location de voitures.
    # Définition des règles d'âge minimum par catégorie de véhicule
    MIN_AGE_BY_CATEGORY = {
        "Véhicule": 18,
        "Camion": 21,
        "Moto": 20,
        "Bus": 25
    }

    def __init__(self):
        self.vehicles: Dict[int, Vehicle] = {}
        self.customers: Dict[int, Customer] = {}
        self.rentals: List[Rental] = []

    # --- Méthodes pour les véhicules ---

    def add_vehicle(self, brand: str, model: str, license_plate: str, daily_rate: float, category: str, state: str) -> Vehicle:
        # Assurez-vous que la classe Vehicle gère la génération d'un ID unique
        vehicle = Vehicle(brand, model, license_plate, daily_rate, category, state)
        self.vehicles[vehicle.id] = vehicle
        return vehicle

    def find_vehicle(self, vehicle_id: int) -> Optional[Vehicle]:
        return self.vehicles.get(vehicle_id)

    def get_all_vehicles(self) -> List[Vehicle]:
        return list(self.vehicles.values())

    def get_available_vehicles(self) -> List[Vehicle]:
        # On suppose que la classe Vehicle a une propriété is_available mise à jour correctement
        # Ou qu'elle dérive de son 'state'
        return [v for v in self.vehicles.values() if v.is_available] # ou v.state.lower() == "disponible"

    def update_vehicle(self, vehicle_id: int, new_brand: str, new_model: str, new_daily_rate: float, new_license_plate: str, new_state: str, new_category: str) -> bool:
        vehicle = self.find_vehicle(vehicle_id)
        if vehicle:
            vehicle.brand = new_brand
            vehicle.model = new_model
            vehicle.daily_rate = new_daily_rate
            vehicle.license_plate = new_license_plate
            vehicle.state = new_state # La classe Vehicle devrait mettre à jour is_available si state change
            if hasattr(vehicle, 'is_available'): # Vérifie si l'attribut existe et le met à jour
                 vehicle.is_available = (new_state.lower() == "disponible")
            return True
        return False

    def remove_vehicle(self, vehicle_id: int) -> bool:
        vehicle = self.find_vehicle(vehicle_id)
        if not vehicle:
            print(f"Erreur: Véhicule avec l'ID {vehicle_id} non trouvé.")
            return False

        # Vérifier s'il existe des locations actives pour ce véhicule
        for rental in self.rentals:
            # On vérifie la présence d'une location dont le véhicule correspond et qui est active
            if rental.vehicle.id == vehicle_id and rental.is_active:
                print(f"Erreur: Véhicule '{vehicle.license_plate}' (ID: {vehicle_id}) est en location active et ne peut pas être supprimé.")
                return False

        del self.vehicles[vehicle_id]
        print(f"Véhicule (ID: {vehicle_id}) supprimé avec succès.")
        return True

    # --- Méthodes pour les clients ---

    def add_customer(self, first_name: str, last_name: str, age: int, driver_license_number: str, email: str) -> Customer:
        # Assurez-vous que la classe Customer gère la génération d'un ID unique
        customer = Customer(first_name, last_name, age, driver_license_number, email)
        self.customers[customer.id] = customer
        return customer

    def find_customer(self, customer_id: int) -> Optional[Customer]:
        return self.customers.get(customer_id)

    def get_all_customers(self) -> List[Customer]:
        return list(self.customers.values())

    def update_customer(self, customer_id: int, new_first_name: str, new_last_name: str, new_age: int, new_driver_license_number: str, new_email: str) -> bool:
        customer = self.find_customer(customer_id)
        if customer:
            customer.first_name = new_first_name
            customer.last_name = new_last_name
            customer.age = new_age
            customer.driver_license_number = new_driver_license_number
            customer.email = new_email
            return True
        return False

    def remove_customer(self, customer_id: int) -> bool:
        print(f"\n--- Tentative de suppression du client ID: {customer_id} ---")

        if customer_id not in self.customers:
            print(f"Erreur: Client avec l'ID {customer_id} non trouvé dans self.customers.")
            return False

        # Vérifier s'il existe des locations actives pour ce client
        found_active_rental = False
        for rental_obj in self.rentals:
            if rental_obj.customer.id == customer_id and rental_obj.is_active:
                print(f"!!! ATTENTION : Location active trouvée pour le client {customer_id} (Location ID: {rental_obj.id}) !!!")
                found_active_rental = True
                break

        if found_active_rental:
            print(f"Erreur: Le client {customer_id} a des locations actives et ne peut pas être supprimé.")
            return False

        del self.customers[customer_id]
        print(f"Client (ID: {customer_id}) supprimé avec succès.")
        return True

    # --- Méthodes pour les locations ---

    def create_rental(self, customer_id: int, vehicle_id: int, start_date: datetime.date, end_date: datetime.date) -> Tuple[Optional[Rental], Optional[str]]:
    
        #Crée une nouvelle location après avoir validé les entrées,
        #la disponibilité du véhicule, l'âge du client et l'absence de chevauchement.
        #Retourne la location créée et None en cas de succès,
        #ou None et un message d'erreur en cas d'échec.
        
        customer = self.find_customer(customer_id)
        vehicle = self.find_vehicle(vehicle_id)

        if not customer:
            return None, f"Erreur: Client avec ID {customer_id} non trouvé."
        if not vehicle:
            return None, f"Erreur: Véhicule avec ID {vehicle_id} non trouvé."

        # 1. Vérification de la disponibilité du véhicule (état et absence de location active)
        if not vehicle.is_available:
            return None, f"Erreur: Véhicule '{vehicle.brand} {vehicle.model}' ({vehicle.license_plate}) non disponible actuellement."

        # 2. Vérification des dates de location
        if end_date < start_date:
            return None, "Erreur: La date de fin ne peut pas être antérieure à la date de début."

        # --- LOGIQUE DE VÉRIFICATION DE L'ÂGE ---
        required_age = self.MIN_AGE_BY_CATEGORY.get(vehicle.category)
        if required_age is not None and customer.age < required_age:
            return None, (f"Erreur: Le client '{customer.first_name} {customer.last_name}' (âge: {customer.age}) "
                          f"n'a pas l'âge minimum requis ({required_age} ans) "
                          f"pour la catégorie de véhicule '{vehicle.category}'.")
        # --- FIN DE LA LOGIQUE DE RÈGLE D'ÂGE ---

        # 3. *** NOUVELLE LOGIQUE : Vérification des chevauchements de dates ***
        for existing_rental in self.rentals:
            # On ne vérifie que les locations pour le même véhicule
            if existing_rental.vehicle.id == vehicle_id:
                # On vérifie si la nouvelle période chevauche une location existante (qui n'est pas encore terminée)
                # Condition de chevauchement :
                # (Début Nouvelle <= Fin Existante) ET (Fin Nouvelle >= Début Existante)
                if start_date < existing_rental.end_date and end_date > existing_rental.start_date:
                    return None, (f"Erreur: Le véhicule '{vehicle.brand} {vehicle.model}' ({vehicle.license_plate}) "
                                  f"est déjà réservé du {existing_rental.start_date.strftime('%d/%m/%Y')} au {existing_rental.end_date.strftime('%d/%m/%Y')}. "
                                  f"Veuillez choisir une autre période ou un autre véhicule.")
        # *** FIN DE LA NOUVELLE LOGIQUE ***


        # Si toutes les validations passent, créer la location
        try:
            rental = Rental(customer, vehicle, start_date, end_date)
            self.rentals.append(rental)

            # Mettre à jour l'état du véhicule pour marquer comme loué
            if hasattr(vehicle, 'set_status'):
                vehicle.set_status("rented")
            elif hasattr(vehicle, 'is_available'):
                vehicle.is_available = False

            # Ajouter la location à l'historique du client
            if hasattr(customer, 'add_rental_to_history'):
                customer.add_rental_to_history(rental.id)

            return rental, None  # Succès, retourne l'objet Rental et aucun message d'erreur

        except Exception as e:
            # Capture d'éventuelles erreurs lors de la création de l'objet Rental ou des mises à jour
            return None, f"Erreur inattendue lors de la création de la location: {e}"


    def find_rental(self, rental_id: int) -> Optional[Rental]:
        for rental in self.rentals:
            if rental.id == rental_id:
                return rental
        return None

    def get_all_rentals(self) -> List[Rental]:
        return self.rentals

    def get_current_rentals(self) -> List[Rental]:
        return [r for r in self.rentals if r.is_active]

    def end_rental(self, rental_id: int, return_date: datetime.date) -> Optional[float]:
        """
        Finalise une location, calcule le coût total (incluant pénalités)
        et met à jour l'état du véhicule.
        Retourne le coût final facturé ou None en cas d'erreur.
        """
        rental = self.find_rental(rental_id)
        if not rental:
            print(f"Erreur: Location ID {rental_id} non trouvée.")
            return None
        if not rental.is_active:
            print(f"Erreur: La location ID {rental_id} n'est pas active et ne peut pas être terminée.")
            return None

        # La logique de validation de la date de retour et de calcul du coût est maintenant dans Rental.calculate_final_cost_on_return
        try:
            final_cost = rental.calculate_final_cost_on_return(return_date)
        except ValueError as e:
            print(f"Erreur lors de la fin de location {rental_id}: {e}")
            return None

        rental.set_status("completed") # Marque la location comme complétée

        # Mettre à jour l'état du véhicule : il devient disponible.
        vehicle = self.find_vehicle(rental.vehicle.id)
        if vehicle:
            # Assumons que si un véhicule est retourné, il redevient disponible.
            # Si le retour tardif avait causé des problèmes au véhicule,
            # il faudrait une logique plus complexe pour le passer en "maintenance".
            vehicle.set_status("available")
            if not hasattr(vehicle, 'set_status') and hasattr(vehicle, 'is_available'): # Fallback si set_status n'existe pas
                 vehicle.is_available = True
        else:
            print(f"Avertissement: Véhicule associé à la location {rental_id} (ID {rental.vehicle.id}) non trouvé lors du retour.")

        print(f"Location {rental_id} terminée. Coût final: {final_cost:.2f}€ (Pénalité: {rental.penalty_amount:.2f}€).")
        return final_cost

    def calculate_total_revenue(self) -> float:
        """
        Calcule le chiffre d'affaires total basé sur les locations terminées
        et dont le montant final a été facturé.
        """
        total = 0.0
        for rental in self.rentals:
            # On additionne seulement les locations terminées (completed)
            # et pour lesquelles un montant final a été enregistré.
            if rental.status == "completed" and rental.final_billed_amount is not None:
                total += rental.final_billed_amount
        return total
