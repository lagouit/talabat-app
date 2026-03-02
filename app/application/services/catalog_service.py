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