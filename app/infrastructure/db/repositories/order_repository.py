from app.infrastructure.db.database_manager import DatabaseManager
from mysql.connector import Error

class OrderRepository:
    """
    REPOSITORY : Gère la persistance des commandes et du séquestre.
    Implémente des transactions ACID pour garantir l'intégrité financière.
    """
    def __init__(self):
        self.__db_manager = DatabaseManager()

    def sauvegarder(self, commande_obj) -> int:
        """
        Sauvegarde une commande complète (Table commandes + Table lignes_commande).
        Utilise une transaction pour éviter les commandes orphelines.
        """
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor()
        try:
            connection.start_transaction()

            # 1. Insertion de l'en-tête de commande
            query_order = """
                INSERT INTO commandes (beneficiaire_id, date_commande, montant_total, statut) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_order, (
                commande_obj.beneficiaire_id, 
                commande_obj.date_commande, 
                commande_obj.montant_total, 
                commande_obj.statut.name
            ))
            order_id = cursor.lastrowid

            # 2. Insertion des lignes de commande (Bulk Insert)
            query_line = """
                INSERT INTO lignes_commande (commande_id, repas_id, quantite, prix_unitaire) 
                VALUES (%s, %s, %s, %s)
            """
            for ligne in commande_obj.lignes:
                cursor.execute(query_line, (order_id, ligne.repas_id, ligne.quantite, ligne.sous_total / ligne.quantite))

            # 3. Initialisation du Séquestre
            query_escrow = "INSERT INTO paiements_sequestre (commande_id, montant, statut) VALUES (%s, %s, 'BLOQUE')"
            cursor.execute(query_escrow, (order_id, commande_obj.montant_total))

            connection.commit()
            return order_id
        except Error as e:
            connection.rollback()
            print(f"❌ Erreur SQL Transactionnelle (sauvegarder) : {e}")
            return None
        finally:
            cursor.close()

    def modifier_statut(self, order_id: int, nouveau_statut: str) -> bool:
        """Met à jour l'état d'avancement de la commande."""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE commandes SET statut = %s WHERE id = %s"
            cursor.execute(query, (nouveau_statut, order_id))
            connection.commit()
            return cursor.rowcount > 0
        except Error:
            connection.rollback()
            return False
        finally:
            cursor.close()

    def liberer_sequestre_vers_fournisseur(self, order_id: int, chef_id: int, montant: float) -> bool:
        """
        Transaction Finale :
        1. Marque le séquestre comme LIBERE.
        2. Crédite le solde du Chef.
        3. Clôture la commande.
        """
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor()
        try:
            connection.start_transaction()
            
            # Libération séquestre
            cursor.execute("UPDATE paiements_sequestre SET statut = 'LIBERE' WHERE commande_id = %s", (order_id,))
            
            # Crédit Fournisseur
            cursor.execute("UPDATE utilisateurs SET solde = solde + %s WHERE id = %s", (montant, chef_id))
            
            # Statut final
            cursor.execute("UPDATE commandes SET statut = 'CONFIRME' WHERE id = %s", (order_id,))
            
            connection.commit()
            return True
        except Error as e:
            connection.rollback()
            print(f"❌ Erreur lors de la libération des fonds : {e}")
            return False
        finally:
            cursor.close()