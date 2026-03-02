from app.core.models.order import Commande, LigneCommande, StatutCommande
from app.utils.factories.notif_factory import FabriqueNotification

class OrderService:
    """
    SERVICE APPLICATIF : Gère le cycle de vie complet d'une commande.
    Respecte le principe de Single Responsibility (SRP).
    """
    def _init_(self, order_repo, payment_processor):
        self.__repo = order_repo
        self.__payment_service = payment_processor

    def passer_commande(self, beneficiaire_id: int, articles_panier: list) -> bool:
        """
        Cas d'utilisation : Transformer un panier en commande officielle.
        1. Création de l'objet métier Commande (Composition).
        2. Calcul du montant total.
        3. Tentative de blocage des fonds (Séquestre).
        4. Persistance en base de données (Transaction SQL).
        """
        if not articles_panier:
            print("⚠️ Le panier est vide.")
            return False

        # 1. Instanciation du modèle domaine
        nouvelle_commande = Commande(id=None, beneficiaire_id=beneficiaire_id)
        
        for art in articles_panier:
            ligne = LigneCommande(
                repas_id=art['repas']['id'],
                titre_repas=art['repas']['titre'],
                quantite=art['quantite'],
                prix_unitaire=art['repas']['prix']
            )
            nouvelle_commande.ajouter_ligne(ligne)

        # 2. Vérification et Blocage des fonds (Interface Abstraite)
        montant = nouvelle_commande.montant_total
        if self.__payment_service.bloquer_fonds(beneficiaire_id, montant):
            
            # 3. Enregistrement via Repository (Gère la transaction SQL)
            nouvelle_commande.statut = StatutCommande.PAYE_SEQUESTRE
            order_id = self.__repo.sauvegarder(nouvelle_commande)
            
            if order_id:
                print(f"✅ Commande #{order_id} validée et fonds sécurisés.")
                # Notification automatique
                notif = FabriqueNotification.notifier("email", "Votre commande est confirmée !")
                notif.envoyer(beneficiaire_id)
                return True
        
        print("❌ Échec du passage de commande (Solde insuffisant ou erreur DB).")
        return False

    def changer_statut_production(self, order_id: int, nouveau_statut: StatutCommande, client_id: int):
        """
        Cas d'utilisation : Le Chef met à jour l'avancement (Prêt, En préparation).
        """
        if self.__repo.modifier_statut(order_id, nouveau_statut.name):
            msg = f"Mise à jour : Votre commande #{order_id} est désormais {nouveau_statut.value}."
            FabriqueNotification.notifier("sms", msg).envoyer(client_id)
            return True
        return False

    def finaliser_livraison(self, order_id: int, chef_id: int, montant: float):
        """
        Cas d'utilisation : Le client confirme la réception.
        Libère l'argent du séquestre vers le compte du fournisseur.
        """
        if self.__repo.liberer_sequestre_vers_fournisseur(order_id, chef_id, montant):
            print(f"💰 Fonds libérés pour le Chef {chef_id}.")
            return True
        return False