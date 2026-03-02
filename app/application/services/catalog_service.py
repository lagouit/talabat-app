class PanierService:
    def __init__(self):
        self.__articles = [] # Composition : le panier contient des items

    def ajouter_au_panier(self, repas: object, quantite: int = 1):
        """Utilisation du Duck Typing : on suppose que 'repas' a un prix et un titre"""
        item = {
            'repas': repas,
            'quantite': quantite,
            'sous_total': repas['prix'] * quantite
        }
        self.__articles.append(item)
        print(f"🛒 {repas['titre']} ajouté au panier.")

    def calculer_total(self) -> float:
        return sum(item['sous_total'] for item in self.__articles)

    def vider(self):
        self.__articles = []

    @property
    def contenu(self):
        return self.__articles
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
