class CatalogService:
    def __init__(self, meal_repo):
        self.repo = meal_repo

    def ajouter_nouveau_plat(self, titre, prix, desc, cat_id, catalogue_id):
        # Logique métier : prix minimum par exemple
        if prix < 10: 
            print("⚠️ Le prix doit être d'au moins 10 DH.")
            return False
        return self.repo.creer(titre, prix, desc, cat_id, catalogue_id)

    def voir_menu(self, catalogue_id):
        return self.repo.lister_par_catalogue(catalogue_id)