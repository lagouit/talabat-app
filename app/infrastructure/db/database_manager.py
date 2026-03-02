import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

class DatabaseManager:
    """
    DESIGN PATTERN : SINGLETON
    Gère la connexion unique à la base de données MySQL.
    """
    _instance = None

    def __new__(cls):
        """Méthode de création de l'instance Singleton"""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._connection = None
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Établit la connexion initiale en utilisant les variables d'environnement"""
        try:
            self._connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD', 'Lagouit123@'),
                database=os.getenv('DB_NAME', 'talabat_db'),
                port=int(os.getenv('DB_PORT', 3306))
            )
            if self._connection.is_connected():
                print("✅ [DatabaseManager] Connexion MySQL établie avec succès.")
        except Error as e:
            print(f"❌ [DatabaseManager] Erreur lors de la connexion : {e}")
            self._connection = None

    def get_connection(self):
        """Retourne l'objet de connexion actif (reconnecte si nécessaire)"""
        if self._connection is None or not self._connection.is_connected():
            print("🔄 [DatabaseManager] Reconnexion à la base de données...")
            self._connect()
        return self._connection

    def close_connection(self):
        """Ferme la connexion proprement à la fin de l'application"""
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("🔌 [DatabaseManager] Connexion MySQL fermée.")

# Utilisation simplifiée : db = DatabaseManager().get_connection()