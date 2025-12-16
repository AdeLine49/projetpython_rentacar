# test_rental.py
import datetime
from models.customer import Customer
from models.vehicle import Vehicle
from models.rental import Rental
from core.car_rental_system import CarRentalSystem

# --- Initialisation ---
system = CarRentalSystem()

# Créer un client de test
customer = system.add_customer("Jean", "Dupont", 30, "1234567890", "jean.dupont@email.com")

# Créer un véhicule de test
# Assurez-vous que les catégories correspondent à MIN_AGE_BY_CATEGORY
vehicle = system.add_vehicle("Renault", "Clio", "AA-001-BB", 50.0, "Véhicule", "disponible") 

# --- Simulation de la location ---
start_date = datetime.date(2025, 12, 10)
end_date = datetime.date(2025, 12, 12) # Date de retour prévue

print(f"--- Création de la location ---")
rental, error_msg = system.create_rental(customer.id, vehicle.id, start_date, end_date)

if rental:
    print(f"Location créée avec succès: {rental}")
    print(f"Coût de base estimé: {rental.get_total_cost():.2f}€")
    print(f"Véhicule status: {vehicle.state}")

    # --- Simulation du retour tardif ---
    actual_return_date = datetime.date(2025, 12, 16) # Retour 4 jours en retard
    print(f"\n--- Tentative de retour du véhicule le {actual_return_date.strftime('%Y-%m-%d')} ---")

    final_billed = system.end_rental(rental.id, actual_return_date)

    if final_billed is not None:
        print(f"\n--- Résultat du retour ---")
        print(f"Coût final facturé pour la location {rental.id}: {final_billed:.2f}€")
        print(f"Montant de la pénalité appliquée: {rental.penalty_amount:.2f}€")
        print(f"Coût total de base prévu initialement: {rental.calculate_base_cost():.2f}€")
        print(f"Véhicule status après retour: {vehicle.state}")
        
        # Afficher les détails de la location après la mise à jour
        print("\nDétails finaux de la location:")
        print(rental)
    else:
        print("Échec de la finalisation de la location.")

else:
    print(f"Échec de la création de la location: {error_msg}")

# --- Test d'un retour à temps ---
print("\n--- Test de retour à temps ---")
vehicle_on_time = system.add_vehicle("Peugeot", "208", "CC-002-DD", 45.0, "Véhicule", "disponible")
start_date_on_time = datetime.date(2025, 12, 20)
end_date_on_time = datetime.date(2025, 12, 22) # Prévu pour 3 jours

rental_on_time, error_msg_on_time = system.create_rental(customer.id, vehicle_on_time.id, start_date_on_time, end_date_on_time)

if rental_on_time:
    actual_return_date_on_time = datetime.date(2025, 12, 22) # Retour le jour prévu
    print(f"Retour effectif le {actual_return_date_on_time.strftime('%Y-%m-%d')}")
    final_billed_on_time = system.end_rental(rental_on_time.id, actual_return_date_on_time)
    
    if final_billed_on_time is not None:
        print(f"Coût final (retour à temps): {final_billed_on_time:.2f}€")
        print(f"Pénalité appliquée: {rental_on_time.penalty_amount:.2f}€") # Devrait être 0.00
        print(rental_on_time)
    else:
        print("Échec du retour à temps.")
else:
    print(f"Échec création location (retour à temps): {error_msg_on_time}")
