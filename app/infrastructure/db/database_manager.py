import mysql.connector
from mysql.connector import Error

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            try:
                # Configuration de la connexion
                cls._instance.connection = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='talabat_db'
                )
                if cls._instance.connection.is_connected():
                    print("✅ Singleton : Connexion MySQL établie.")
            except Error as e:
                print(f"❌ Singleton : Erreur de connexion : {e}")
                cls._instance.connection = None
        return cls._instance

    def get_connection(self):
        """Retourne l'objet de connexion unique."""
        return self.connection