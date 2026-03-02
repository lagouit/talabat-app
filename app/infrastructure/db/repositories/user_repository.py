from app.infrastructure.db.database_manager import DatabaseManager
from mysql.connector import Error

class UserRepository:
    """
    REPOSITORY : Centralise tout le SQL lié aux utilisateurs.
    Sépare la logique de stockage de la logique métier (Domaine).
    """
    def __init__(self):
        # Utilisation du Singleton pour récupérer la connexion
        self.__db_manager = DatabaseManager()

    def trouver_par_email(self, email: str):
        """Récupère un utilisateur brut depuis la DB via son email"""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT * FROM utilisateurs WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone()
        except Error as e:
            print(f"❌ Erreur SQL (trouver_par_email) : {e}")
            return None
        finally:
            cursor.close()

    def creer_utilisateur(self, nom: str, email: str, mdp_hache: str, role: str, details: dict) -> int:
        """
        Insère un nouvel utilisateur et ses détails spécifiques.
        Gère la transaction pour garantir l'intégrité des données.
        """
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor()
        try:
            # 1. Insertion dans la table générique 'utilisateurs'
            query_user = """
                INSERT INTO utilisateurs (nom, email, mot_de_passe, role) 
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_user, (nom, email, mdp_hache, role))
            user_id = cursor.lastrowid

            # 2. Insertion des détails spécifiques selon le rôle (Exemple pour le Client)
            if role == "beneficiaire":
                query_client = """
                    INSERT INTO clients (utilisateur_id, adresse_livraison, telephone) 
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query_client, (user_id, details.get('adresse'), details.get('tel')))
            
            # 3. Insertion pour le Fournisseur (Chef)
            elif role == "fournisseur":
                query_chef = """
                    INSERT INTO fournisseurs (utilisateur_id, biographie) 
                    VALUES (%s, %s)
                """
                cursor.execute(query_chef, (user_id, details.get('bio')))

            connection.commit()
            return user_id
        except Error as e:
            connection.rollback()
            print(f"❌ Erreur SQL (creer_utilisateur) : {e}")
            return None
        finally:
            cursor.close()

    def mettre_a_jour_solde(self, user_id: int, nouveau_solde: float):
        """Met à jour le portefeuille financier d'un utilisateur"""
        connection = self.__db_manager.get_connection()
        cursor = connection.cursor()
        try:
            query = "UPDATE utilisateurs SET solde = %s WHERE id = %s"
            cursor.execute(query, (nouveau_solde, user_id))
            connection.commit()
            return True
        except Error as e:
            connection.rollback()
            return False
        finally:
            cursor.close()