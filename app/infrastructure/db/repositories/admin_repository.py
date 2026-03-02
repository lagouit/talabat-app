from app.infrastructure.db.database_manager import DatabaseManager

class AdminRepository:
    def __init__(self):
        self.__db = DatabaseManager().get_connection()

    def lister_kyc_en_attente(self):
        cursor = self.__db.cursor(dictionary=True)
        query = "SELECT d.*, u.nom FROM documents_kyc d JOIN utilisateurs u ON d.fournisseur_id = u.id WHERE d.est_valide = FALSE"
        cursor.execute(query)
        return cursor.fetchall()

    def valider_fournisseur(self, fournisseur_id: int):
        cursor = self.__db.cursor()
        try:
            # On valide le document ET le statut du fournisseur
            cursor.execute("UPDATE documents_kyc SET est_valide = TRUE WHERE fournisseur_id = %s", (fournisseur_id,))
            cursor.execute("UPDATE utilisateurs SET kyc_valide = TRUE WHERE id = %s", (fournisseur_id,))
            self.__db.commit()
            return True
        except Exception as e:
            self.__db.rollback()
            return False

    def ajouter_categorie(self, libelle: str):
        cursor = self.__db.cursor()
        cursor.execute("INSERT INTO categories (libelle) VALUES (%s)", (libelle,))
        self.__db.commit()
    
    def ajouter_document_kyc(self, fournisseur_id: int, type_doc: str, url: str) -> bool:
        cursor = self.__db.cursor()
        query = """INSERT INTO documents_kyc (fournisseur_id, type_doc, fichier_url) 
                   VALUES (%s, %s, %s)"""
        try:
            cursor.execute(query, (fournisseur_id, type_doc, url))
            self.__db.commit()
            return True
        except Exception as e:
            print(f"❌ Erreur SQL KYC : {e}")
            return False
    
    def obtenir_stats_ventes(self):
        """Requête SQL agrégée (SUM, COUNT)"""
        cursor = self.__db.cursor(dictionary=True)
        query = """
            SELECT 
                COUNT(id) as total_commandes,
                SUM(montant_total) as chiffre_affaires,
                AVG(montant_total) as panier_moyen
            FROM commandes 
            WHERE statut = 'CONFIRME'
        """
        cursor.execute(query)
        return cursor.fetchone()

    def enregistrer_note(self, commande_id: int, note: int, commentaire: str):
        cursor = self.__db.cursor()
        query = "INSERT INTO evaluations (commande_id, note, commentaire) VALUES (%s, %s, %s)"
        cursor.execute(query, (commande_id, note, commentaire))
        self.__db.commit()
   
