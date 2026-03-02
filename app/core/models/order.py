from enum import Enum
from abc import ABC, abstractmethod

# 1. Machine à états (Enum)
class StatutCommande(Enum):
    ATTENTE_PAIEMENT = "Attente Paiement"
    PAYE_SEQUESTRE = "Payé (Séquestre)"
    ACCEPTE_CHEF = "Accepté par le Chef"
    EN_PREPARATION = "En Préparation"
    PRET_LIVRAISON = "Prêt pour Livraison"
    LIVRE = "Livré"
    CONFIRME = "Confirmé par Client"
    ANNULE = "Annulé"