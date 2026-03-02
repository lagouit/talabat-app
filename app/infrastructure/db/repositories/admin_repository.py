from app.infrastructure.db.database_manager import DatabaseManager
from mysql.connector import Error

class AdminRepository:
    """
    REPOSITORY : Fournit les outils de gestion et de statistiques à l'Admin.
    Centralise les requêtes de surveillance et de modération.
    """
    def __init__(self):
        self.__db_manager = DatabaseManager()

    def obtenir_fournisseurs_en_attente(self):
        """Récupère la liste des chefs qui n'ont pas encore été validés par l'admin."""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                SELECT u.id, u.nom, u.email, f.biographie 
                FROM utilisateurs u
                JOIN fournisseurs f ON u.id = f.utilisateur_id
                WHERE f.kyc_valide = 0
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def activer_fournisseur(self, chef_id: int) -> bool:
        """Valide officiellement le compte d'un chef."""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE fournisseurs SET kyc_valide = 1 WHERE utilisateur_id = %s"
            cursor.execute(query, (chef_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error:
            connection.rollback()
            return False
        finally:
            cursor.close()

    def ajouter_categorie(self, libelle: str) -> bool:
        """Insère une nouvelle catégorie de menu dans le système."""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor()
        try:
            query = "INSERT INTO categories (libelle) VALUES (%s)"
            cursor.execute(query, (libelle,))
            connection.commit()
            return True
        except Error:
            connection.rollback()
            return False
        finally:
            cursor.close()

    def calculer_statistiques_globales(self) -> dict:
        """
        Agrégation SQL pour le tableau de bord Admin.
        Récupère le CA, le nombre d'utilisateurs et de commandes.
        """
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        stats = {}
        try:
            # Compte des utilisateurs
            cursor.execute("SELECT COUNT(*) as total FROM utilisateurs")
            stats['users_count'] = cursor.fetchone()['total']

            # Chiffre d'affaires total (uniquement les commandes confirmées)
            cursor.execute("SELECT SUM(montant_total) as CA FROM commandes WHERE statut = 'CONFIRME'")
            res_ca = cursor.fetchone()
            stats['total_revenue'] = res_ca['CA'] if res_ca['CA'] else 0.0

            # Commandes passées aujourd'hui
            cursor.execute("SELECT COUNT(*) as j FROM commandes WHERE DATE(date_commande) = CURDATE()")
            stats['orders_today'] = cursor.fetchone()['j']

            return stats
        except Error as e:
            print(f"❌ Erreur Stats Admin : {e}")
            return {"users_count": 0, "total_revenue": 0.0, "orders_today": 0}
        finally:
            cursor.close()