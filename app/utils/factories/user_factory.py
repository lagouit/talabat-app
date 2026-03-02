from app.core.models.user import Beneficiaire, Fournisseur, Administrateur

class FabriqueUtilisateur:
    @staticmethod
    def creer_utilisateur(type_user: str, donnees: dict):
        """
        Instancie un utilisateur selon son rôle.
        Utilise le Type Hinting pour la clarté.
        """
        role = type_user.lower()
        
        if role == "beneficiaire":
            return Beneficiaire(
                id=donnees.get('id'),
                nom=donnees.get('nom'),
                email=donnees.get('email'),
                mot_de_passe=donnees.get('mot_de_passe'),
                adresse_livraison=donnees.get('adresse'),
                telephone=donnees.get('telephone')
            )
        elif role == "fournisseur":
            return Fournisseur(
                id=donnees.get('id'),
                nom=donnees.get('nom'),
                email=donnees.get('email'),
                mot_de_passe=donnees.get('mot_de_passe'),
                biographie=donnees.get('biographie')
            )
        elif role == "admin":
            return Administrateur(
                id=donnees.get('id'),
                nom=donnees.get('nom'),
                email=donnees.get('email'),
                mot_de_passe=donnees.get('mot_de_passe')
            )
        return None