from app.utils.factories.notif_factory import FabriqueNotification

class OrderService:
    # ... (méthodes précédentes)
    
    def mettre_a_jour_production(self, order_id: int, client_id: int, statut: StatutCommande):
        # 1. Mise à jour DB
        if self.repo.modifier_statut(order_id, statut.name):
            # 2. Déclenchement Notification via Factory
            msg = f"Le statut de votre commande #{order_id} est passé à : {statut.value}"
            notif = FabriqueNotification.notifier("email", msg)
            if notif:
                notif.envoyer(client_id)
            return True
        return False
class SequestreService(PaymentProcessor):
    def _init_(self, order_repo):
        self.repo = order_repo

    def bloquer_fonds(self, utilisateur_id: int, montant: float, commande_id: int) -> bool:
        """Implémentation concrète de l'abstraction"""
        return self.repo.executer_sequestre(utilisateur_id, montant, commande_id)

    def liberer_fonds(self, transaction_id: str) -> bool:
        # Implémenté dans l'US10 lors de la livraison
        pass
from app.core.models.order import Commande, LigneCommande

class OrderService:
    def _init_(self, order_repo):
        self.repo = order_repo

    def valider_panier(self, beneficiaire_id: int, articles_panier: list):
        if not articles_panier:
            return None

        # Création de l'objet métier Commande
        nouvelle_commande = Commande(id=None, beneficiaire_id=beneficiaire_id)
        
        for art in articles_panier:
            ligne = LigneCommande(
                repas_id=art['repas']['id'],
                quantite=art['quantite'],
                prix_unitaire=art['repas']['prix']
            )
            nouvelle_commande.ajouter_ligne(ligne)

        # Persistance via Repository
        return self.repo.creer_commande(nouvelle_commande)
