from app.core.models.meal import Repas, Categorie, Catalogue
from typing import List, Optional

class CatalogService:
    """
    SERVICE APPLICATIF : Gère l'exposition du menu et la mise à jour des plats.
    Utilise le Repository pour la persistance et les Modèles pour la logique.
    """
    def __init__(self, meal_repo):
        self.__repo = meal_repo

    # --- PARTIE FOURNISSEUR (Chef) ---

    def ajouter_plat_au_menu(self, chef_id: int, titre: str, description: str, prix: float, categorie_id: int) -> bool:
        """Cas d'utilisation : Un chef ajoute un nouveau plat à son catalogue."""
        if prix <= 0:
            print("⚠️ Le prix doit être positif.")
            return False
            
        return self.__repo.creer_repas(chef_id, titre, description, prix, categorie_id)

    def modifier_disponibilite(self, repas_id: int, disponible: bool) -> bool:
        """Cas d'utilisation : Marquer un plat comme épuisé ou disponible."""
        return self.__repo.mettre_a_jour_statut(repas_id, disponible)

    # --- PARTIE BÉNÉFICIAIRE (Client) ---

    def consulter_par_categorie(self, libelle_categorie: str) -> List[dict]:
        """
        Cas d'utilisation : Filtrer les plats disponibles par catégorie.
        Retourne une liste de dictionnaires (Data Transfer Objects).
        """
        plats = self.__repo.filtrer_par_categorie(libelle_categorie)
        if not plats:
            print(f"ℹ️ Aucun plat disponible dans la catégorie '{libelle_categorie}'.")
        return plats

    def obtenir_details_repas(self, repas_id: int) -> Optional[dict]:
        """Récupère les informations complètes d'un plat spécifique."""
        return self.__repo.trouver_par_id(repas_id)

    def lister_tous_les_repas(self) -> List[dict]:
        """Affiche l'ensemble de la carte disponible sur la plateforme."""
        return self.__repo.lister_actifs()

    # --- GESTION DES CATÉGORIES (Admin/Global) ---

    def recuperer_categories(self) -> List[dict]:
        """Récupère la liste des catégories existantes pour les menus déroulants."""
        return self.__repo.lister_categories()