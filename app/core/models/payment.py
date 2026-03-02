from abc import ABC, abstractmethod
from datetime import datetime

class PaymentProcessor(ABC):
    """
    INTERFACE ABSTRAITE (Domaine)
    Définit le contrat pour tout processeur de paiement (Séquestre, Stripe, PayPal).
    Respecte le principe OCP (Open/Closed Principle).
    """
    @abstractmethod
    def bloquer_fonds(self, commande_id: int, montant: float) -> bool:
        """Méthode pour sécuriser l'argent du client au moment de la commande"""
        pass

    @abstractmethod
    def liberer_fonds(self, commande_id: int) -> bool:
        """Méthode pour verser l'argent au fournisseur après confirmation"""
        pass

    @abstractmethod
    def rembourser(self, commande_id: int) -> bool:
        """Méthode en cas d'annulation de la commande"""
        pass

class PaiementSequestre:
    """
    ENTITÉ MÉTIER : Représente une transaction sécurisée.
    Utilise l'encapsulation pour protéger le montant.
    """
    def _init_(self, id: int, commande_id: int, montant: float):
        self.id = id
        self.commande_id = commande_id
        self.__montant = montant  # Attribut privé
        self.date_creation = datetime.now()
        self.est_libere = False
        self.est_rembourse = False

    @property
    def montant(self) -> float:
        """Accès en lecture seule au montant bloqué"""
        return self.__montant

    def marquer_comme_libere(self):
        """Logique métier : On ne peut pas libérer un paiement déjà remboursé"""
        if not self.est_rembourse:
            self.est_libere = True
        else:
            raise Exception("Impossible de libérer un fonds déjà remboursé.")

    def _str_(self):
        statut = "Libéré" if self.est_libere else "Bloqué (Séquestre)"
        if self.est_rembourse: statut = "Remboursé"
        return f"Transaction #{self.id} | Commande: {self.commande_id} | Montant: {self.__montant} DH | Statut: {statut}"