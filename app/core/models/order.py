from datetime import datetime
from typing import List

class LigneCommande:
    def _init_(self, repas_id: int, quantite: int, prix_unitaire: float):
        self.repas_id = repas_id
        self.quantite = quantite
        self.prix_unitaire_fixe = prix_unitaire

class Commande:
    def _init_(self, id: int, beneficiaire_id: int, statut: str = 'ATTENTE_PAIEMENT'):
        self.id = id
        self.beneficiaire_id = beneficiaire_id
        self.date_creation = datetime.now()
        self.statut = statut
        self.__lignes: List[LigneCommande] = [] # Composition
        self.__montant_total = 0.0

    def ajouter_ligne(self, ligne: LigneCommande):
        self.__lignes.append(ligne)
        self.__calculer_total()

    def __calculer_total(self):
        """Automatisation du calcul du montant total"""
        self._montant_total = sum(l.quantite * l.prix_unitaire_fixe for l in self._lignes)

    @property
    def montant_total(self):
        return self.__montant_total

    @property
    def lignes((self)):
        return self.__lignes