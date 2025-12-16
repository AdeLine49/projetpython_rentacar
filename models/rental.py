import datetime
from typing import Optional
from models.customer import Customer
from models.vehicle import Vehicle

class Rental:
    _next_id = 1

    def __init__(self, customer: Customer, vehicle: Vehicle, start_date: datetime.date, end_date: datetime.date):
        self.id = Rental._next_id
        Rental._next_id += 1
        self.customer = customer
        self.vehicle = vehicle
        self.start_date = start_date
        self.end_date = end_date # Date de retour prévue
        self.status = "active" # Statut initial : active, completed, cancelled
        self.is_active = True
        self.final_billed_amount: Optional[float] = None
        self.actual_return_date: Optional[datetime.date] = None
        self.penalty_amount: float = 0.0 

    def set_status(self, status: str):
        self.status = status
        self.is_active = (status == "active")

    def calculate_base_cost(self) -> float:
        """Calcule le coût de base de la location basé sur la durée prévue."""
        # Le coût de base est calculé sur la durée prévue initialement
        duration_days = (self.end_date - self.start_date).days + 1
        return self.vehicle.daily_rate * duration_days

    def calculate_final_cost_on_return(self, return_date: datetime.date) -> float:
    
        #Calcule le coût final de la location au moment du retour effectif,
        #incluant la pénalité de retard. Met à jour la date de retour effective,
        #le montant de la pénalité et le montant facturé final.
    
        if return_date < self.start_date:
            raise ValueError("La date de retour ne peut pas être antérieure à la date de début de location.")

        self.actual_return_date = return_date

        # Calculer le coût basé sur la durée effective pour le tarif journalier initial
        effective_duration_days = (self.actual_return_date - self.start_date).days + 1
        base_cost_effective_duration = self.vehicle.daily_rate * effective_duration_days

        # --- LOGIQUE DE PÉNALITÉ DE RETARD ---
        self.penalty_amount = 0.0 # Réinitialiser la pénalité avant calcul

        # Si la date de retour effective est APRES la date de retour prévue
        if self.actual_return_date > self.end_date:
            # Calculer les jours de retard
            # On ajoute 1 car si on rend le 2 au lieu du 1, c'est 1 jour de retard
            days_late = (self.actual_return_date - self.end_date).days
            
            if days_late > 0:
                # Définir le montant de la pénalité par jour de retard
                # Vous pouvez ajuster cette valeur (ex: 20.0, 50.0, etc.)
                PENALTY_PER_DAY = 20.0 
                self.penalty_amount = days_late * PENALTY_PER_DAY

        # Le coût final est le coût basé sur la durée effective + la pénalité
        cost = base_cost_effective_duration + self.penalty_amount

        self.final_billed_amount = cost # Stocke le coût final
        return cost

    def get_total_cost(self) -> float:
        
        #Retourne le coût total facturé si la location est terminée (avec pénalités incluses),
        #sinon retourne le coût de base estimé basé sur la durée prévue.
        
        if self.final_billed_amount is not None:
            return self.final_billed_amount
        return self.calculate_base_cost()

    def __str__(self):
        return (f"Rental ID: {self.id}, Vehicle: {self.vehicle.brand} {self.vehicle.model} (ID: {self.vehicle.id}), "
                f"Customer: {self.customer.first_name} {self.customer.last_name} (ID: {self.customer.id}), "
                f"Start: {self.start_date.strftime('%Y-%m-%d')}, End: {self.end_date.strftime('%Y-%m-%d')}, "
                f"Status: {self.status}, "
                f"Final Billed: {self.final_billed_amount if self.final_billed_amount is not None else 'N/A'}€, "
                f"Penalty: {self.penalty_amount:.2f}€, "
                f"Actual Return: {self.actual_return_date.strftime('%Y-%m-%d') if self.actual_return_date else 'N/A'}")
