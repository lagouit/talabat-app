from app.infrastructure.db.database_manager import DatabaseManager
from mysql.connector import Error

class MealRepository:
    """
    REPOSITORY : Gère les opérations CRUD pour les repas et catégories.
    Isole les requêtes SQL du reste de l'application.
    """
    def __init__(self):
        self.__db_manager = DatabaseManager()

    def lister_categories(self):
        """Récupère toutes les catégories disponibles pour les menus."""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, libelle FROM categories ORDER BY libelle")
            return cursor.fetchall()
        finally:
            cursor.close()

    def creer_repas(self, chef_id, titre, description, prix, categorie_id) -> bool:
        """Insère un nouveau plat en base de données."""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO repas (fournisseur_id, titre, description, prix, categorie_id, disponible) 
                VALUES (%s, %s, %s, %s, %s, 1)
            """
            cursor.execute(query, (chef_id, titre, description, prix, categorie_id))
            connection.commit()
            return True
        except Error as e:
            connection.rollback()
            print(f"❌ Erreur SQL (creer_repas) : {e}")
            return False
        finally:
            cursor.close()

    def lister_actifs(self):
        """Récupère tous les plats disponibles avec leur catégorie (JOIN)."""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                SELECT r.id, r.titre, r.description, r.prix, c.libelle as categorie, r.fournisseur_id
                FROM repas r
                JOIN categories c ON r.categorie_id = c.id
                WHERE r.disponible = 1
            """
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def filtrer_par_categorie(self, libelle_cat: str):
        """Recherche de plats par nom de catégorie."""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = """
                SELECT r.*, c.libelle 
                FROM repas r
                JOIN categories c ON r.categorie_id = c.id
                WHERE c.libelle LIKE %s AND r.disponible = 1
            """
            cursor.execute(query, (f"%{libelle_cat}%",))
            return cursor.fetchall()
        finally:
            cursor.close()

    def mettre_a_jour_statut(self, repas_id: int, disponible: bool):
        """Active ou désactive la visibilité d'un plat."""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE repas SET disponible = %s WHERE id = %s"
            cursor.execute(query, (1 if disponible else 0, repas_id))
            connection.commit()
            return cursor.rowcount > 0
        except Error:
            connection.rollback()
            return False
        finally:
            cursor.close()