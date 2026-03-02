from app.infrastructure.db.database_manager import DatabaseManager

class UserRepository:
    def __init__(self):
        self.__db = DatabaseManager().get_connection()

    def sauvegarder(self, user_data: dict, role: str):
        cursor = self.__db.cursor()
        query = """INSERT INTO utilisateurs (nom, email, mot_de_passe, role) 
                   VALUES (%s, %s, %s, %s)"""
        try:
            cursor.execute(query, (user_data['nom'], user_data['email'], 
                                   user_data['mdp_hache'], role))
            self.__db.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"❌ Erreur SQL : {e}")
            return None

    def trouver_par_email(self, email: str):
        cursor = self.__db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
        return cursor.fetchone()