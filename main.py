import datetime
from core.car_rental_system import CarRentalSystem
from models.vehicle import Car, Truck, Motorcycle

def main():
    system = CarRentalSystem()

    print("--- Ajout de véhicules ---")
    car1 = system.add_vehicle("car", "Toyota", "Corolla", 50.0, num_seats=5)
    car2 = system.add_vehicle("car", "Honda", "Civic", 60.0, num_seats=5)
    truck1 = system.add_vehicle("truck", "Ford", "F-150", 120.0, cargo_capacity_kg=1000)
    moto1 = system.add_vehicle("motorcycle", "Yamaha", "MT-07", 70.0, engine_cc=689)
    print("\n")

    print("--- Ajout de clients ---")
    client1 = system.add_customer("Alice", "Dupont", 25, "AD12345")
    client2 = system.add_customer("Bob", "Martin", 19, "BM67890") # Age insuffisant pour moto et camion par défaut
    client3 = system.add_customer("Charles", "Durand", 30, "CD11223")
    print("\n")

    print("--- Vérification des véhicules disponibles ---")
    print("Véhicules disponibles:")
    for v in system.get_available_vehicles():
        print(f"- {v}")
    print("\n")

    print("--- Création de locations ---")
    rental1 = system.create_rental(client1.id, car1.id, "2025-01-10", "2025-01-15") # Client 1 loue voiture 1
    rental2 = system.create_rental(client3.id, truck1.id, "2025-01-12", "2025-01-17") # Client 3 loue camion 1
    
    # Tentative de location avec âge insuffisant
    rental3 = system.create_rental(client2.id, moto1.id, "2025-01-10", "2025-01-13") 
    
    # Tentative de louer un véhicule déjà loué
    rental4 = system.create_rental(client1.id, car1.id, "2025-01-16", "2025-01-20") 
    print("\n")

    print("--- Locations en cours ---")
    for r in system.get_current_rentals():
        print(f"- {r}")
    print("\n")

    print("--- Simulation de fin de location ---")
    if rental1:
        print(f"Fin de la location {rental1.id} pour {rental1.customer.first_name} (retour à temps)")
        system.end_rental(rental1.id, actual_end_date_str="2025-01-15")
    
    if rental2:
        print(f"Fin de la location {rental2.id} pour {rental2.customer.first_name} (retour tardif)")
        # Simuler un retour 2 jours après la date prévue
        system.end_rental(rental2.id, actual_end_date_str="2025-01-19") 
    print("\n")

    print("--- Vérification des véhicules disponibles après retours ---")
    print("Véhicules disponibles:")
    for v in system.get_available_vehicles():
        print(f"- {v}")
    print("\n")

    print("--- Chiffre d'affaires total ---")
    print(f"Chiffre d'affaires total: {system.calculate_total_revenue():.2f}€")
    print("\n")

    print("--- Historique de location du client Alice ---")
    alice_history = system.get_customer_rental_history(client1.id)
    if alice_history:
        for r in alice_history:
            print(f"- {r}")
    else:
        print("Aucun historique pour Alice.")
    print("\n")

    print("--- Statistiques du système ---")
    stats = system.get_rental_statistics()
    for key, value in stats.items():
        print(f"- {key.replace('_', ' ').capitalize()}: {value}")
    print("\n")

    print("--- Gestion de l'entretien (option avancée) ---")
    print(f"Statut de {car2.brand} {car2.model} avant maintenance: {car2.status}")
    system.record_vehicle_maintenance(car2.id)
    print(f"Statut de {car2.brand} {car2.model} après maintenance: {car2.status}")
    print("\n")

if __name__ == "__main__":
    main()
