def menu_admin(admin_service):
    while True:
        print("\n--- PANNEAU D'ADMINISTRATION ---")
        print("1. Valider les documents KYC")
        print("2. Ajouter une catégorie de repas")
        print("3. Quitter")
        
        choix = input("Action : ")
        
        if choix == "1":
            docs = admin_service.repo.lister_kyc_en_attente()
            if not docs:
                print("ℹ️ Aucun document en attente.")
            else:
                for d in docs:
                    print(f"ID Chef: {d['fournisseur_id']} | Nom: {d['nom']} | Doc: {d['type_doc']}")
                
                f_id = input("\nEntrez l'ID du chef à valider (ou 'r') : ")
                if f_id != 'r' and admin_service.approuver_chef(int(f_id)):
                    print("✅ Chef validé avec succès.")

        elif choix == "2":
            nom = input("Nom de la nouvelle catégorie : ")
            if admin_service.creer_categorie(nom):
                print(f"✅ Catégorie '{nom}' créée.")
        
        elif choix == "3":
            break