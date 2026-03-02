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