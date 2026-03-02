import os
from app.presentation.cli.client_ui import ClientUI
from app.presentation.cli.chef_ui import ChefUI
from app.presentation.cli.admin_ui import AdminUI

class MainMenu:
    """
    ROUTEUR PRINCIPAL (CLI) : Orchestre la navigation globale.
    Vérifie l'état d'authentification et délègue aux UI spécialisées.
    """
    def _init_(self, auth_service, catalog_service, order_service, admin_service):
        self.auth = auth_service
        self.catalog = catalog_service
        self.order = order_service
        self.admin = admin_service

    def nettoyer_console(self):
        """Efface le terminal selon le système d'exploitation."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def afficher_menu_principal(self):
        """Boucle de contrôle principale de l'application."""
        while True:
            self.nettoyer_console()
            print("==========================================")
            print("        🍴 PLATEFORME TALABAT 🍴         ")
            print("==========================================")
            
            user = self.auth.utilisateur_connecte
            
            if not user:
                # Mode Visiteur / Non connecté
                print("1. Se connecter")
                print("2. Créer un compte")
                print("q. Quitter l'application")
                
                choix = input("\nSelectionnez une option : ")
                if choix == '1': self._flux_connexion()
                elif choix == '2': self._flux_inscription()
                elif choix.lower() == 'q': break
            else:
                # Mode Connecté : Redirection par rôle
                role_name = user._class.name_
                print(f"👤 Bienvenue, {user.nom} | Rôle : {role_name}")
                print("------------------------------------------")
                
                if role_name == "Beneficiaire":
                    ui = ClientUI(self.catalog, self.order, user)
                    ui.menu_principal()
                elif role_name == "Fournisseur":
                    ui = ChefUI(self.catalog, self.order, user)
                    ui.menu_principal()
                elif role_name == "Administrateur":
                    ui = AdminUI(self.admin, self.catalog)
                    ui.menu_principal()
                
                # Option de déconnexion commune une fois sorti des sous-menus
                print("\nd. Se déconnecter")
                print("q. Quitter")
                post_choix = input("\nChoix : ")
                if post_choix.lower() == 'd': 
                    self.auth.deconnexion()
                elif post_choix.lower() == 'q':
                    break

    # --- FLUX D'ACCÈS ---

    def _flux_connexion(self):
        print("\n--- AUTHENTIFICATION ---")
        email = input("📧 Email : ")
        mdp = input("🔑 Mot de passe : ")
        if self.auth.connexion(email, mdp):
            print("✅ Connexion réussie.")
        else:
            print("❌ Identifiants invalides.")
        input("\nAppuyez sur Entrée...")

    def _flux_inscription(self):
        print("\n--- CRÉATION DE COMPTE ---")
        nom = input("👤 Nom complet : ")
        email = input("📧 Email : ")
        mdp = input("🔑 Mot de passe : ")
        print("\nType de compte :")
        print("1. Client (Bénéficiaire)")
        print("2. Chef (Fournisseur)")
        
        type_compte = input("Choix : ")
        role = "beneficiaire" if type_compte == '1' else "fournisseur"
        
        details = {}
        if role == "beneficiaire":
            details['adresse'] = input("🏠 Adresse de livraison : ")
            details['tel'] = input("📱 Numéro de téléphone : ")
        else:
            details['bio'] = input("👨‍🍳 Présentez votre cuisine (bio) : ")

        if self.auth.inscription(nom, email, mdp, role, details):
            print("✅ Inscription réussie ! Vous pouvez maintenant vous connecter.")
        else:
            print("❌ Échec de l'inscription (Email déjà utilisé ?).")
        input("\nAppuyez sur Entrée...")