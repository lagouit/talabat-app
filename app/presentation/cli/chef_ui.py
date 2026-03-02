from app.infrastructure.db.repositories.admin_repository import AdminRepository

def menu_soumission_kyc(fournisseur_id: int):
    print("\n--- SOUMISSION DES DOCUMENTS KYC ---")
    type_doc = input("Type de document (CIN/Passeport) : ")
    nom_fichier = input("Nom du fichier à uploader (ex: cin_recto.pdf) : ")
    
    # Simulation du chemin de stockage
    url_simulee = f"storage/kyc/user_{fournisseur_id}/{nom_fichier}"
    
    repo = AdminRepository()
    if repo.ajouter_document_kyc(fournisseur_id, type_doc, url_simulee):
        print(f"✅ Document '{type_doc}' envoyé pour validation.")
    else:
        print("❌ Échec de l'envoi.")