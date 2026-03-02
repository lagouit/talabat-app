
def confirmer_commande_ui(order_service, client_id):
    print("\n--- CONFIRMATION DE RÉCEPTION ---")
    oid = int(input("Entrez l'ID de la commande reçue : "))
    # Dans la vraie app, on récupère le montant et le chef_id via l'ID commande
    if order_service.confirmer_reception(oid, chef_id=12, montant=150.0):
        print("✅ Merci ! Les fonds ont été libérés au Chef.")
    else:
        print("❌ Une erreur est survenue lors de la confirmation.")
        
def menu_beneficiaire(auth_service, meal_repo, panier_service):
    while True:
        print("\n--- ESPACE BÉNÉFICIAIRE ---")
        print("1. Parcourir les plats par catégorie")
        print("2. Voir mon panier")
        print("3. Quitter")
        
        choix = input("Choix : ")
        
        if choix == "1":
            cat = input("Entrez la catégorie (ex: Pizza) : ")
            plats = meal_repo.filtrer_par_categorie(cat)
            for p in plats:
                print(f"ID: {p['id']} | {p['titre']} - {p['prix']} DH")
            
            p_id = input("\nID du plat à ajouter (ou 'r' pour retour) : ")
            if p_id != 'r':
                # Simulation de récupération de l'objet plat choisi
                plat_choisi = next(p for p in plats if str(p['id']) == p_id)
                panier_service.ajouter_au_panier(plat_choisi)

        elif choix == "2":
            print("\n--- VOTRE PANIER ---")
            for item in panier_service.contenu:
                print(f"- {item['repas']['titre']} x{item['quantite']} : {item['sous_total']} DH")
            print(f"TOTAL : {panier_service.calculer_total()} DH")
        
        elif choix == "3":
            break