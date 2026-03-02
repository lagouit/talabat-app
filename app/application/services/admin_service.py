class AdminService:
    def __init__(self, admin_repo):
        self.repo = admin_repo

    def approuver_chef(self, fournisseur_id: int):
        # Logique : On pourrait ajouter ici l'envoi d'une notification automatique
        return self.repo.valider_fournisseur(fournisseur_id)

    def creer_categorie(self, libelle: str):
        if len(libelle) < 3:
            print("⚠️ Le libellé est trop court.")
            return False
        return self.repo.ajouter_categorie(libelle)