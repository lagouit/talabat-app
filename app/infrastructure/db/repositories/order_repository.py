# À ajouter dans OrderRepository

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
    def finaliser_paiement_fournisseur(self, commande_id: int, chef_id: int, montant: float) -> bool:
        cursor = self.__db.cursor()
        try:
            self.__db.start_transaction()
            
            # 1. Clôturer le séquestre
            cursor.execute("UPDATE paiements_sequestre SET statut = 'LIBERE' WHERE commande_id = %s", (commande_id,))
            
            # 2. Créditer le fournisseur
            cursor.execute("UPDATE utilisateurs SET solde = solde + %s WHERE id = %s", (montant, chef_id))
            
            # 3. Marquer la commande comme CONFIRMEE
            cursor.execute("UPDATE commandes SET statut = 'CONFIRME' WHERE id = %s", (commande_id,))
            
            self.__db.commit()
            return True
        except Exception as e:
            self.__db.rollback()
            print(f"❌ Erreur libération fonds : {e}")
            return False
   
    def executer_sequestre(self, client_id: int, montant: float, commande_id: int) -> bool:
        cursor = self.__db.cursor()
        try:
            self.__db.start_transaction()
            
            # 1. Vérification et débit du solde client
            cursor.execute("UPDATE utilisateurs SET solde = solde - %s WHERE id = %s AND solde >= %s", 
                        (montant, client_id, montant))
            
            if cursor.rowcount == 0:
                raise Exception("Solde insuffisant")

            # 2. Création de l'enregistrement de séquestre
            query = "INSERT INTO paiements_sequestre (commande_id, montant, statut) VALUES (%s, %s, 'BLOQUE')"
            cursor.execute(query, (commande_id, montant))
            
            self.__db.commit()
            return True
        except Exception as e:
            self.__db.rollback()
            print(f"❌ Échec séquestre : {e}")
            return False