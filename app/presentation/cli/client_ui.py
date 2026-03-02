from app.core.models.order import StatutCommande

class ClientUI:
    """
    Interface dédiée aux clients (Bénéficiaires).
    Gère le panier temporaire et les interactions avec le catalogue.
    """
    def _init_(self, catalog_service, order_service, user_session):
        self.catalog = catalog_service
        self.order_service = order_service
        self.user = user_session
        self.panier = [] # Liste de dictionnaires {'repas': dict, 'quantite': int}

    def menu_principal(self):
        while True:
            print(f"\n--- ESPACE CLIENT : {self.user.nom} ---")
            print(f"💰 Solde : {getattr(self.user, 'solde', 0)} DH")
            print("1. Parcourir le catalogue")
            print("2. Rechercher par catégorie")
            print("3. Voir mon panier")
            print("4. Historique de mes commandes")
            print("r. Retour au menu principal")
            
            choix = input("\nVotre choix : ")
            if choix == '1': self._afficher_catalogue()
            elif choix == '2': self._rechercher_categorie()
            elif choix == '3': self._gerer_panier()
            elif choix == 'r': break

    def _afficher_catalogue(self):
        print("\n--- CARTE DU JOUR ---")
        plats = self.catalog.lister_tous_les_repas()
        if not plats:
            print("Aucun plat n'est disponible pour le moment.")
            return

        for p in plats:
            print(f"[{p['id']}] {p['titre']} - {p['prix']} DH ({p['categorie']})")
        
        id_choisi = input("\nID du plat à ajouter au panier (ou Entrée pour annuler) : ")
        if id_choisi.isdigit():
            self._ajouter_au_panier(int(id_choisi), plats)

    def _ajouter_au_panier(self, plat_id, liste_plats):
        plat = next((p for p in liste_plats if p['id'] == plat_id), None)
        if plat:
            qte = int(input(f"Quantité pour '{plat['titre']}' : ") or 1)
            self.panier.append({'repas': plat, 'quantite': qte})
            print(f"✅ {plat['titre']} ajouté au panier.")
        else:
            print("❌ ID invalide.")

    def _gerer_panier(self):
        if not self.panier:
            print("\n🛒 Votre panier est vide.")
            return

        print("\n--- VOTRE PANIER ---")
        total = 0
        for i, item in enumerate(self.panier):
            sous_total = item['repas']['prix'] * item['quantite']
            total += sous_total
            print(f"{i+1}. {item['repas']['titre']} x{item['quantite']} = {sous_total} DH")
        
        print(f"\nTOTAL A PAYER : {total} DH")
        print("1. Valider la commande (Paiement Séquestre)")
        print("2. Vider le panier")
        print("3. Retour")

        choix = input("\nAction : ")
        if choix == '1':
            if self.order_service.passer_commande(self.user.id, self.panier):
                self.panier = [] # Vider après succès
        elif choix == '2':
            self.panier = []
            print("🛒 Panier vidé.")

    def _rechercher_categorie(self):
        cat = input("Nom de la catégorie (ex: Marocain, Pizza) : ")
        plats = self.catalog.consulter_par_categorie(cat)
        for p in plats:
            print(f"[{p['id']}] {p['titre']} - {p['prix']} DH")
        input("\nAppuyez sur Entrée")