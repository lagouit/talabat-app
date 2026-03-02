from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def bloquer_fonds(self, utilisateur_id: int, montant: float) -> bool:
        """Méthode abstraite pour sécuriser la transaction"""
        pass

    @abstractmethod
    def liberer_fonds(self, transaction_id: str) -> bool:
        """Méthode abstraite pour verser l'argent au fournisseur"""
        pass

class PaiementSequestre(PaymentProcessor):
    def _init_(self, transaction_id: str, montant: float):
        self.transaction_id = transaction_id
        self.__montant = montant # Encapsulation privée
        self.est_bloque = True

    @property
    def montant(self):
        return self.__montant