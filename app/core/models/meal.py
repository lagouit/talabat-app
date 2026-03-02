from typing import List, Optional

class Categorie:
    """
    Entité représentant une catégorie de plat (ex: Entrée, Plat, Dessert, Marocain).
    """
    def __init__(self, id: int, libelle: str):
        self.id = id
        self.libelle = libelle

    def __str__(self):
        return f"Catégorie: {self.libelle}"

class Repas:
    """
    Entité représentant un plat spécifique proposé par un fournisseur.
    """
    def __init__(self, id: int, titre: str, description: str, prix: float, categorie: Categorie, fournisseur_id: int):
        self.id = id
        self.titre = titre
        self.description = description
        self.__prix = prix  # Encapsulation : prix privé
        self.categorie = categorie # Association avec Categorie
        self.fournisseur_id = fournisseur_id
        self.est_disponible = True

    # Getter pour le prix
    @property
    def prix(self) -> float:
        return self.__prix

    # Setter avec validation métier
    @prix.setter
    def prix(self, nouveau_prix: float):
        if nouveau_prix > 0:
            self.__prix = nouveau_prix
        else:
            raise ValueError("Le prix doit être strictement positif.")

    def __str__(self):
        return f"{self.titre} ({self.prix} DH) - {self.categorie.libelle}"

class Catalogue:
    """
    Entité représentant le menu global d'un fournisseur (Chef).
    Concept : Agrégation de plusieurs objets Repas.
    """
    def __init__(self, id: int, nom_menu: str, fournisseur_id: int):
        self.id = id
        self.nom_menu = nom_menu
        self.fournisseur_id = fournisseur_id
        self.__liste_repas: List[Repas] = [] # Liste privée de repas

    def ajouter_repas(self, repas: Repas):
        """Ajoute un repas au catalogue s'il appartient au même fournisseur"""
        if repas.fournisseur_id == self.fournisseur_id:
            self.__liste_repas.append(repas)
        else:
            raise Exception("Ce repas n'appartient pas à ce fournisseur.")

    def retirer_repas(self, repas_id: int):
        self.__liste_repas = [r for r in self.__liste_repas if r.id != repas_id]

    @property
    def repas_disponibles(self) -> List[Repas]:
        """Retourne uniquement les plats marqués comme disponibles"""
        return [r for r in self.__liste_repas if r.est_disponible]

    def obtenir_par_categorie(self, libelle_cat: str) -> List[Repas]:
        """Filtre les repas du catalogue par catégorie"""
        return [r for r in self.__liste_repas if r.categorie.libelle.lower() == libelle_cat.lower()]