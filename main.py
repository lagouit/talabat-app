import sys
import os

# Ajout du dossier racine au PYTHONPATH pour résoudre les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infrastructure.db.database_manager import DatabaseManager
from app.infrastructure.db.repositories.user_repository import UserRepository
from app.infrastructure.db.repositories.meal_repository import MealRepository
from app.infrastructure.db.repositories.order_repository import OrderRepository
from app.infrastructure.db.repositories.admin_repository import AdminRepository

from app.application.services.auth_service import AuthService
from app.application.services.catalog_service import CatalogService
from app.application.services.order_service import OrderService
from app.application.services.admin_service import AdminService

from app.presentation.cli.main_menu import MainMenu

def bootstraper_application():
    """
    Initialise tous les composants du système.
    Suit le flux : DB -> Repositories -> Services -> UI.
    """
    try:
        # 1. Initialisation de l'Infrastructure (Accès aux données)
        user_repo = UserRepository()
        meal_repo = MealRepository()
        order_repo = OrderRepository()
        admin_repo = AdminRepository()

        # 2. Initialisation de la Couche Application (Logique métier)
        # On injecte ici les repositories nécessaires à chaque service
        auth_service = AuthService(user_repo)
        catalog_service = CatalogService(meal_repo)
        
        # Note : OrderService nécessite aussi un processeur de paiement
        # Pour le MVP, on passe le repository en guise de simulateur simple
        order_service = OrderService(order_repo, payment_processor=user_repo) 
        
        admin_service = AdminService(admin_repo)

        # 3. Initialisation de la Couche Présentation (Interface utilisateur)
        interface_utilisateur = MainMenu(
            auth_service, 
            catalog_service, 
            order_service, 
            admin_service
        )
        
        return interface_utilisateur

    except Exception as e:
        print(f"❌ Erreur critique lors de l'initialisation : {e}")
        return None

if __name__ == "__main__":
    # Nettoyage console au démarrage
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("******************************************")
    print("* BIENVENUE SUR TALABAT APP 🍴      *")
    print("* Architecture N-Tier & SOLID       *")
    print("******************************************")

    app = bootstraper_application()

    if app:
        try:
            # Lancement du menu principal (Boucle infinie)
            app.afficher_menu_principal()
        except KeyboardInterrupt:
            print("\n\n👋 Arrêt manuel détecté. Fermeture sécurisée...")
        finally:
            # On s'assure de fermer la connexion MySQL via le Singleton
            DatabaseManager().close_connection()
            print("💤 Application terminée.")
    else:
        print("🛑 Impossible de démarrer l'application. Vérifiez vos fichiers .env et SQL.")