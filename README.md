# Système de Location de Voitures

Ce projet implémente un système de gestion de location de voitures basé sur les principes de la programmation orientée objet (POO) en Python. L'application est développée avec Streamlit pour l'interface utilisateur.

## Objectif Général

L'objectif est de développer une application permettant à une agence de location de :
*   Gérer son parc automobile (ajout, suppression, suivi de l'état et des détails des véhicules).
*   Gérer ses clients (ajout, suivi de leur historique de location).
*   Effectuer et suivre les locations (réservation, retour).
*   Calculer le coût d'une location, incluant d'éventuelles pénalités.
*   Générer divers rapports et statistiques pour aider à la prise de décision.

## Fonctionnalités Implémentées

1.  **Gestion de la Flotte Automobile**
    *   Classes `Vehicle`, `Car`, `Truck`, `Motorcycle` avec des attributs tels que `id`, `brand` (marque), `model` (modèle), `category` (catégorie), `daily_rate` (tarif journalier), `status` (statut).
    *   Gestion du statut du véhicule : `available` (disponible), `rented` (loué), `maintenance` (en maintenance).
    *   *Précision :* L'attribut `brand` remplace l'ancien `make` pour la marque du véhicule.

2.  **Gestion des Clients**
    *   Classe `Customer` avec `id`, `first_name` (prénom), `last_name` (nom), `age` (âge), `driver_license_number` (numéro de permis de conduire), et un historique des locations (`rentals_history`).
    *   Règles d'âge minimum appliquées lors de la création d'une location, ces règles peuvent varier selon le type de véhicule.

3.  **Système de Réservation (Location)**
    *   Classe `Rental` pour enregistrer les détails de la location : `id`, `customer`, `vehicle`, `start_date` (date de début), `end_date` (date de fin), `penalty_amount` (montant de la pénalité), `status` (statut de la location).
    *   Calcul automatique du coût total de la location.
    *   Application de pénalités, que ce soit manuellement ou automatiquement (par exemple, pour un retour tardif).
    *   Vérification de la disponibilité du véhicule et de la validité des dates avant de confirmer une location.

4.  **Classe Centrale `CarRentalSystem`**
    *   Cette classe agit comme le cœur du système, gérant les collections de véhicules, clients et locations.
    *   Elle expose des méthodes pour ajouter, récupérer, supprimer et mettre à jour les entités (véhicules, clients, locations).
    *   Contient la logique métier essentielle pour le processus de création et de clôture des locations.

## Rapports Générés

*   Liste des véhicules actuellement disponibles.
*   Liste des locations en cours.
*   Calcul du chiffre d'affaires total généré par l'agence.
*   Historique détaillé des locations pour un client spécifique.
*   Statistiques globales sur l'activité de location (nombre total de locations, locations complétées, locations en cours, véhicules les plus populaires, etc.).

## Interface Utilisateur avec Streamlit

*   Des pages dédiées sont implémentées pour les différentes fonctionnalités :
    *   Page principale pour afficher les informations générales.
    *   Pages pour ajouter/gérer les véhicules, clients et locations.
    *   Pages pour visualiser les rapports.
*   Utilisation de `st.rerun()` pour rafraîchir l'interface utilisateur après des actions importantes (comme la création d'une nouvelle location).

## Comment Exécuter

1.  Assurez-vous d'avoir Python 3.x installé sur votre système.
2.  Clonez le dépôt GitHub de ce projet.
3.  Naviguez jusqu'au répertoire racine du projet dans votre terminal.
4.  Exécutez l'application Streamlit :
    ```bash
    streamlit run app.py
    ```
## Diagramme de Classes UML

Le diagramme de Classes a été fait avec l'aide de StarUML.  

## Tests Unitaires

Démonstration au tableau :
- CRUD pour la gestion des clients et gestion des véhicules fonctionnels.
- Location en cours et nouvelles locations fonctionnels
- Limite d'âge pour un véhicule fonctionnel, ex avec l'ajout du client Juliette et une moto avec un âge de 18 ans.
- Fonctionnalités rapports fonctionnels.
- Terminer une location.
- Exécution du script test_rental.py fonctionnel pour appliquer la pénalité de retard dans le terminal python.
