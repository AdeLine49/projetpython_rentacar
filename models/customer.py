import datetime

class Customer:
    """
    Représente un client de l'agence de location.
    """
    _next_id = 1 # Compteur pour générer des IDs uniques pour tous les clients

    def __init__(self, first_name: str, last_name: str, age: int, driver_license_number: str, email: str):
        # L'ID n'est plus passé en argument, il est généré en interne.
        if not all([first_name, last_name, driver_license_number, email]):
            raise ValueError("Le prénom, le nom, le numéro de permis et l'email du client doivent être fournis.")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("L'âge doit être un entier positif.")
        if "@" not in email or "." not in email: # Validation basique de l'email
            raise ValueError("Le format de l'email est invalide.")

        self.id = Customer._next_id # L'ID est généré automatiquement
        Customer._next_id += 1      # Incrémente le compteur pour le prochain client

        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.driver_license_number = driver_license_number
        self.email = email
        self.rentals_history: list[int] = [] # Liste des IDs de location (de type int) pour le suivi

    def __str__(self):
        return (f"ID Client: {self.id}, Nom: {self.first_name} {self.last_name}, "
                f"Âge: {self.age}, Permis: {self.driver_license_number}, Email: {self.email}")

    def add_rental_to_history(self, rental_id: int): # L'ID de location est maintenant un int
        if rental_id not in self.rentals_history:
            self.rentals_history.append(rental_id)
