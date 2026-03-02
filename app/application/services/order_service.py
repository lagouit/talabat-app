class SequestreService(PaymentProcessor):
    def _init_(self, order_repo):
        self.repo = order_repo

    def bloquer_fonds(self, utilisateur_id: int, montant: float, commande_id: int) -> bool:
        """Implémentation concrète de l'abstraction"""
        return self.repo.executer_sequestre(utilisateur_id, montant, commande_id)

    def liberer_fonds(self, transaction_id: str) -> bool:
        # Implémenté dans l'US10 lors de la livraison
        pass