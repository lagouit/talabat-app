from app.core.models.order import StatutCommande

class ChefUI:
    """
    Interface dédiée aux Fournisseurs (Chefs).
    Permet la gestion du catalogue personnel et le suivi de la production.
    """
    def __init__(self, catalog_service, order_service, user_session):
        self.catalog = catalog_service
        self.order_service = order_service
        self.user = user_session

    def menu_principal(self):
        while True:
            print(f"\n--- ESPACE CHEF : {self.user.nom} ---")
            print(f"💰 Portefeuille : {self.user.solde_accumule} DH")
            print(f"✅ Statut KYC : {'Validé' if self.user.kyc_valide else 'En attente'}")
            print("-----------------------------------")
            print("1. Ajouter un nouveau plat au menu")
            print("2. Gérer la disponibilité de mes plats")
            print("3. Voir les commandes à préparer")
            print("4. Historique des ventes")
            print("r. Retour au menu principal")
            
            choix = input("\nVotre choix : ")
            if choix == '1': self._ajouter_plat()
            elif choix == '2': self._gerer_disponibilite()
            elif choix == '3': self._voir_commandes_actives()
            elif choix == 'r': break

    def _ajouter_plat(self):
        if not self.user.kyc_valide:
            print("⚠️ Votre compte doit être validé par un admin pour publier des plats.")
            return

        print("\n--- NOUVEAU PLAT ---")
        titre = input("Nom du plat : ")
        desc = input("Description : ")
        try:
            prix = float(input("Prix (DH) : "))
            # On affiche les catégories disponibles
            cats = self.catalog.recuperer_categories()
            for c in cats:
                print(f"[{c['id']}] {c['libelle']}")
            cat_id = int(input("Sélectionnez l'ID de la catégorie : "))

            if self.catalog.ajouter_plat_au_menu(self.user.id, titre, desc, prix, cat_id):
                print("✅ Plat ajouté avec succès !")
        except ValueError:
            print("❌ Erreur : Veuillez saisir des valeurs numériques valides.")

    def _gerer_disponibilite(self):
        print("\n--- MES PLATS ---")
        # Note: On suppose une méthode pour lister les plats d'un chef spécifique
        plats = self.catalog.lister_tous_les_repas() 
        mes_plats = [p for p in plats if p['fournisseur_id'] == self.user.id]

        for p in mes_plats:
            print(f"[{p['id']}] {p['titre']} - Disponible: Oui")
        
        id_plat = input("\nID du plat à modifier (ou Entrée pour annuler) : ")
        if id_plat:
            etat = input("Rendre disponible ? (o/n) : ").lower() == 'o'
            if self.catalog.modifier_disponibilite(int(id_plat), etat):
                print("✅ Mise à jour effectuée.")

    def _voir_commandes_actives(self):
        print("\n--- COMMANDES EN ATTENTE DE PRÉPARATION ---")
        # Simulation d'affichage des commandes liées au chef
        print("Commande #102 - Couscous Royal (x2) - Statut: PAYE_SEQUESTRE")
        print("1. Marquer comme 'En préparation'")
        print("2. Marquer comme 'Prêt pour livraison'")
        
        choix = input("\nAction : ")
        if choix in ['1', '2']:
            nouveau_statut = StatutCommande.EN_PREPARATION if choix == '1' else StatutCommande.PRET_LIVRAISON
            # Appel au service pour changer le statut
            # self.order_service.changer_statut_production(102, nouveau_statut, client_id=45)
            print(f"✅ Commande mise à jour vers : {nouveau_statut.value}")