import hashlib

class AuthService:
    def __init__(self, user_repo):
        self.repo = user_repo

    def hacher_mot_de_passe(self, password: str) -> str:
        """Hachage sécurisé SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def inscription(self, nom, email, password, role):
        # Vérifier si l'utilisateur existe déjà
        if self.repo.trouver_par_email(email):
            print("⚠️ Cet email est déjà utilisé.")
            return False
        
        mdp_hache = self.hacher_mot_de_passe(password)
        user_data = {'nom': nom, 'email': email, 'mdp_hache': mdp_hache}
        
        return self.repo.sauvegarder(user_data, role)

    def connexion(self, email, password):
        user = self.repo.trouver_par_email(email)
        if user and user['mot_de_passe'] == self.hacher_mot_de_passe(password):
            print(f"✅ Bienvenue {user['nom']} !")
            return user
        print("❌ Identifiants incorrects.")
        return None