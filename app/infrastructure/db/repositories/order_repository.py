from app.infrastructure.db.database_manager import DatabaseManager

class OrderRepository:
    def _init_(self):
        self.__db = DatabaseManager().get_connection()

    def creer_commande(self, commande_obj: object) -> int:
        cursor = self.__db.cursor()
        try:
            # Début de la transaction
            self.__db.start_transaction()

            # 1. Insertion de la commande
            query_order = """INSERT INTO commandes (beneficiaire_id, montant_total, statut, date_creation) 
                             VALUES (%s, %s, %s, %s)"""
            cursor.execute(query_order, (commande_obj.beneficiaire_id, commande_obj.montant_total, 
                                         commande_obj.statut, commande_obj.date_creation))
            
            commande_id = cursor.lastrowid

            # 2. Insertion des lignes (Composition)
            query_line = """INSERT INTO lignes_commande (commande_id, repas_id, quantite, prix_unitaire) 
                            VALUES (%s, %s, %s, %s)"""
            
            for ligne in commande_obj.lignes:
                cursor.execute(query_line, (commande_id, ligne.repas_id, 
                                            ligne.quantite, ligne.prix_unitaire_fixe))

            # Validation de la transaction
            self.__db.commit()
            return commande_id

        except Exception as e:
            # Annulation en cas d'erreur
            self.__db.rollback()
            print(f"❌ Erreur Transaction Commande : {e}")
            return None