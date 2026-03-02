from app.utils.factories.notif_factory import FabriqueNotification

class AdminService:
    """
    SERVICE APPLICATIF : Gère les privilèges administratifs.
    Assure la modération des comptes et l'organisation du catalogue.
    """
    def __init__(self, admin_repo):
        self.__repo = admin_repo

    # --- GESTION DES FOURNISSEURS (KYC) ---

    def lister_demandes_validation(self):
        """Récupère les chefs ayant soumis leurs documents mais non encore validés."""
        return self.__repo.obtenir_fournisseurs_en_attente()

    def valider_compte_chef(self, chef_id: int) -> bool:
        """
        Cas d'utilisation : L'admin approuve un nouveau fournisseur.
        1. Met à jour le statut en base de données.
        2. Notifie le chef de l'activation de son compte.
        """
        if self.__repo.activer_fournisseur(chef_id):
            print(f"✅ Le compte du chef #{chef_id} a été validé.")
            
            # Notification de succès
            notif = FabriqueNotification.notifier("email", "Félicitations ! Votre compte Chef est désormais actif.")
            notif.envoyer(chef_id)
            return True
        
        print(f"❌ Erreur lors de la validation du compte #{chef_id}.")
        return False

    # --- GESTION DU CATALOGUE ---

    def creer_nouvelle_categorie(self, libelle: str) -> bool:
        """Ajoute une catégorie globale (ex: 'Végétarien', 'Pâtisserie')."""
        if len(libelle.strip()) < 3:
            print("⚠️ Le libellé de la catégorie est trop court.")
            return False
        
        return self.__repo.ajouter_categorie(libelle)

    # --- STATISTIQUES & SURVEILLANCE ---

    def obtenir_tableau_de_bord(self) -> dict:
        """Récupère les indicateurs clés de performance (KPI) de la plateforme."""
        stats = self.__repo.calculer_statistiques_globales()
        return {
            "total_utilisateurs": stats.get('users_count', 0),
            "commandes_du_jour": stats.get('orders_today', 0),
            "chiffre_affaires_total": stats.get('total_revenue', 0.0),
            "taux_annulation": stats.get('cancellation_rate', 0)
        }