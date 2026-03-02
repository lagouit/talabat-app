from app.infrastructure.db.database_manager import DatabaseManager

class AdminRepository:
    def __init__(self):
        self.__db = DatabaseManager().get_connection()

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