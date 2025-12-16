import datetime

class Vehicle:
    #Classe de base pour représenter un véhicule dans le système.
    _next_id = 1  # Compteur pour générer des IDs uniques pour tous les véhicules

    def __init__(self, brand: str, model: str, license_plate: str, daily_rate: float,
                 category: str, state: str):
        # Vérifications initiales
        if not all([brand, model, license_plate, category, state]):
            raise ValueError("La marque, le modèle, la plaque d'immatriculation, la catégorie et l'état du véhicule doivent être fournis.")
        if not isinstance(daily_rate, (int, float)) or daily_rate <= 0:
            raise ValueError("Le tarif journalier doit être un nombre positif.")

        self.id = Vehicle._next_id # L'ID est généré automatiquement
        Vehicle._next_id += 1      # Incrémente le compteur pour le prochain véhicule

        self.brand = brand
        self.model = model
        self.license_plate = license_plate
        self.daily_rate = daily_rate
        self.category = category
        self.state = state
        self.status = "available"  
        self.last_maintenance_date = None
        self.rental_history = []

    def __str__(self):
        return (f"ID: {self.id}, Marque: {self.brand}, Modèle: {self.model}, "
                f"Catégorie: {self.category}, Plaque: {self.license_plate}, "
                f"Tarif/jour: {self.daily_rate}€, Statut: {self.status}, État: {self.state}")

    def is_available(self) -> bool:
        """Vérifie si le véhicule est disponible pour la location."""
        return self.status == "available"

    def set_status(self, new_status: str):
        """Met à jour le statut du véhicule."""
        if new_status not in ["available", "rented", "maintenance"]:
            raise ValueError("Statut de véhicule invalide.")
        self.status = new_status

    def record_maintenance(self):
        """Enregistre une date de maintenance et met le véhicule en statut 'maintenance'."""
        self.last_maintenance_date = datetime.date.today()
        self.set_status("maintenance")

class Car(Vehicle):
    """Représente une voiture."""
    def __init__(self, brand: str, model: str, license_plate: str, daily_rate: float,
                 state: str, num_seats: int): 
        super().__init__(brand, model, license_plate, daily_rate, "Car", state) 
        self.num_seats = num_seats

    def __str__(self):
        return f"{super().__str__()} (Places: {self.num_seats})"

class Truck(Vehicle):
    """Représente un camion."""
    def __init__(self, brand: str, model: str, license_plate: str, daily_rate: float,
                 state: str, cargo_capacity_kg: float): 
        super().__init__(brand, model, license_plate, daily_rate, "Truck", state)  
        self.cargo_capacity_kg = cargo_capacity_kg

    def __str__(self):
        return f"{super().__str__()} (Capacité de charge: {self.cargo_capacity_kg} kg)"

class Motorcycle(Vehicle):
    """Représente une moto."""
    def __init__(self, brand: str, model: str, license_plate: str, daily_rate: float,
                 state: str, engine_cc: int): 
        super().__init__(brand, model, license_plate, daily_rate, "Motorcycle", state) 
        self.engine_cc = engine_cc

    def __str__(self):
        return f"{super().__str__()} (Moteur: {self.engine_cc} cc)"
