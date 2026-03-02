from enum import Enum
from datetime import datetime
from typing import List

class StatutCommande(Enum):
    """Machine à états pour le flux de production"""
    ATTENTE_PAIEMENT = "Attente de Paiement"
    PAYE_SEQUESTRE = "Payé (En Séquestre)"
    EN_PREPARATION = "En cours de préparation"
    PRET_LIVRAISON = "Prêt pour livraison"
    LIVRE = "Livré"
    CONFIRME = "Confirmé par Client"
    ANNULE = "Annulé"

class LigneCommande:
    """
    Détail d'un produit dans une commande.
    Note : Le prix est fixé au moment de la commande (immutabilité).
    """
    def _init_(self, repas_id: int, titre_repas: str, quantite: int, prix_unitaire: float):
        self.repas_id = repas_id
        self.titre_repas = titre_repas
        self.quantite = quantite
        self.__prix_unitaire_fixe = prix_unitaire # Prix au moment de l'achat

    @property
    def sous_total(self) -> float:
        return self.quantite * self.__prix_unitaire_fixe

class Commande:
    """
    Entité Commande. 
    Concept : Composition (Les lignes de commande appartiennent exclusivement à une commande).
    """
    def _init_(self, id: Optional[int], beneficiaire_id: int):
        self.id = id
        self.beneficiaire_id = beneficiaire_id
        self.date_commande = datetime.now()
        self.__statut = StatutCommande.ATTENTE_PAIEMENT
        self.__lignes: List[LigneCommande] = [] # Composition
        self.__montant_total = 0.0

    def ajouter_ligne(self, ligne: LigneCommande):
        """Ajoute un produit et recalcule le total automatiquement"""
        if self.__statut == StatutCommande.ATTENTE_PAIEMENT:
            self.__lignes.append(ligne)
            self.__calculer_total()
        else:
            raise Exception("Impossible de modifier une commande déjà validée.")

    def __calculer_total(self):
        """Met à jour le montant total de la commande"""
        self._montant_total = sum(l.sous_total for l in self._lignes)

    @property
    def montant_total(self) -> float:
        return self.__montant_total

    @property
    def statut(self) -> StatutCommande:
        return self.__statut

    @statut.setter
    def statut(self, nouveau_statut: StatutCommande):
        """Permet de faire évoluer la commande dans le flux de production"""
        self.__statut = nouveau_statut

    @property
    def lignes(self) -> List[LigneCommande]:
        return self.__lignes

    def _str_(self):
        return f"Commande #{self.id} | Client: {self.beneficiaire_id} | Total: {self.montant_total} DH | Statut: {self.__statut.value}"