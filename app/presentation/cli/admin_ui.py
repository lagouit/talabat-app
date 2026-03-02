class AdminUI:
    """
    Interface dédiée à l'Administrateur système.
    Permet la validation KYC, la gestion des catégories et le reporting.
    """
    def __init__(self, admin_service, catalog_service):
        self.admin_service = admin_service
        self.catalog_service = catalog_service

    def menu_principal(self):
        while True:
            print("\n--- 🛡️ PANNEAU D'ADMINISTRATION ---")
            print("1. Valider les nouveaux comptes Chefs (KYC)")
            print("2. Consulter le tableau de bord (KPI)")
            print("3. Gérer les catégories de produits")
            print("4. Lister tous les utilisateurs")
            print("r. Retour au menu principal")
            
            choix = input("\nVotre choix : ")
            if choix == '1': self._valider_chefs()
            elif choix == '2': self._afficher_stats()
            elif choix == '3': self._gerer_categories()
            elif choix == 'r': break

    def _valider_chefs(self):
        print("\n--- DEMANDES DE VALIDATION EN ATTENTE ---")
        demandes = self.admin_service.lister_demandes_validation()
        
        if not demandes:
            print("✅ Aucune demande en attente.")
            return

        for d in demandes:
            print(f"ID: {d['id']} | Nom: {d['nom']} | Bio: {d['biographie'][:50]}...")
        
        id_chef = input("\nEntrez l'ID du chef à valider (ou Entrée pour annuler) : ")
        if id_chef.isdigit():
            if self.admin_service.valider_compte_chef(int(id_chef)):
                print(f"✅ Le chef #{id_chef} a été activé.")

    def _afficher_stats(self):
        print("\n--- 📊 INDICATEURS DE PERFORMANCE (KPI) ---")
        stats = self.admin_service.obtenir_tableau_de_bord()
        
        print(f"• Utilisateurs inscrits   : {stats.get('total_utilisateurs', 0)}")
        print(f"• Commandes aujourd'hui   : {stats.get('orders_today', 0)}")
        print(f"• Volume d'affaires (CA)  : {stats.get('total_revenue', 0.0):.2f} DH")
        print(f"• Taux d'annulation       : {stats.get('cancellation_rate', 0)}%")
        input("\nAppuyez sur Entrée pour fermer le rapport...")

    def _gerer_categories(self):
        print("\n--- GESTION DES CATÉGORIES ---")
        print("Catégories actuelles :")
        cats = self.catalog_service.recuperer_categories()
        for c in cats:
            print(f"- {c['libelle']}")
        
        nouveau_libelle = input("\nNom de la nouvelle catégorie (ou Entrée pour annuler) : ")
        if nouveau_libelle:
            if self.admin_service.creer_nouvelle_categorie(nouveau_libelle):
                print(f"✅ Catégorie '{nouveau_libelle}' ajoutée.")