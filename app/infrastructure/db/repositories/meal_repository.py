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