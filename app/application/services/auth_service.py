import hashlib
from app.utils.factories.user_factory import UserFactory
from app.infrastructure.db.repositories.user_repository import UserRepository

class AuthService:
    """
    SERVICE APPLICATIF : Gère l'authentification et la sécurité des comptes.
    Fait le lien entre le Repository (Données) et la Factory (Objets).
    """
    def __init__(self, user_repo: UserRepository):
        self.__repo = user_repo
        self.__current_user = None # Session utilisateur active

    def __hacher_mot_de_passe(self, password: str) -> str:
        """Sécurité : Hachage SHA-256 (ne jamais stocker en clair)"""
        return hashlib.sha256(password.encode()).hexdigest()

    def inscription(self, nom: str, email: str, password: str, role: str, details_specifiques: dict) -> bool:
        """
        Logique d'inscription :
        1. Hache le mot de passe.
        2. Prépare les données pour le Repository.
        3. Enregistre en base de données via SQL natif.
        """
        if self.__repo.trouver_par_email(email):
            print(f"⚠️ Erreur : L'email {email} est déjà utilisé.")
            return False

        mdp_hache = self.__hacher_mot_de_passe(password)
        
        # On délègue la sauvegarde au Repository
        user_id = self.__repo.creer_utilisateur(nom, email, mdp_hache, role, details_specifiques)
        
        if user_id:
            print(f"✅ Inscription réussie pour {nom} (ID: {user_id})")
            return True
        return False

    def connexion(self, email: str, password: str) -> bool:
        """
        Logique de connexion :
        1. Récupère les données brutes SQL.
        2. Vérifie le hash du mot de passe.
        3. Utilise la Factory pour transformer le résultat SQL en Objet Domaine.
        """
        user_data = self.__repo.trouver_par_email(email)
        
        if user_data and user_data['mot_de_passe'] == self.__hacher_mot_de_passe(password):
            # Transformation du dictionnaire SQL en Objet (Bénéficiaire, Fournisseur ou Admin)
            self.__current_user = UserFactory.creer_utilisateur(user_data['role'], user_data)
            print(f"🔓 Connexion réussie : Bienvenue {self.__current_user.nom} !")
            return True
        
        print("❌ Échec de connexion : Email ou mot de passe incorrect.")
        return False

    def deconnexion(self):
        """Réinitialise la session"""
        self.__current_user = None
        print("🔒 Déconnexion effectuée.")

    @property
    def utilisateur_connecte(self):
        """Retourne l'objet Domaine de l'utilisateur actuel"""
        return self.__current_user