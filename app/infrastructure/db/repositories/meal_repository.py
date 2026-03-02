from app.infrastructure.db.database_manager import DatabaseManager

class MealRepository:
    def __init__(self):
        self.__db = DatabaseManager().get_connection()

    def filtrer_par_categorie(self, libelle_cat: str):
        """Recherche SQL native avec jointure"""
        cursor = self.__db.cursor(dictionary=True)
        query = """
            SELECT r.*, c.libelle FROM repas r
            JOIN categories c ON r.categorie_id = c.id
            WHERE c.libelle LIKE %s AND r.est_disponible = TRUE
        """
        cursor.execute(query, (f"%{libelle_cat}%",))
        return cursor.fetchall()
    def creer(self, titre, prix, desc, cat_id, catalogue_id):
        cursor = self.__db.cursor()
        query = "INSERT INTO repas (titre, prix, description, categorie_id, catalogue_id) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (titre, prix, desc, cat_id, catalogue_id))
        self.__db.commit()
        return cursor.lastrowid

    def lister_par_catalogue(self, catalogue_id):
        cursor = self.__db.cursor(dictionary=True)
        query = "SELECT * FROM repas WHERE catalogue_id = %s"
        cursor.execute(query, (catalogue_id,))
        return cursor.fetchall()

    def supprimer(self, repas_id):
        cursor = self.__db.cursor()
        cursor.execute("DELETE FROM repas WHERE id = %s", (repas_id,))
        self.__db.commit()
