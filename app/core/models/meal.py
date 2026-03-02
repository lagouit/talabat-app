from typing import List

class Categorie:
    def __init__(self, id: int, libelle: str):
        self.id = id
        self.libelle = libelle

class Repas:
    def __init__(self, id: int, titre: str, prix: float, description: str, categorie: Categorie):
        self.id = id
        self.titre = titre
        self.__prix = prix  # Encapsulation
        self.description = description
        self.categorie = categorie
        self.est_disponible = True

    def modifier_prix(self, nouveau_prix: float):
        if nouveau_prix > 0:
            self.__prix = nouveau_prix

    @property
    def prix(self):
        return self.__prix

class Catalogue:
    def __init__(self, id: int, nom_menu: str):
        self.id = id
        self.nom_menu = nom_menu
        self.__repas_liste: List[Repas] = [] # Agrégation

    def ajouter_repas(self, r: Repas):
        self.__repas_liste.append(r)