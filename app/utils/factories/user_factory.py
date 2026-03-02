from app.core.models.user import Beneficiaire, Fournisseur, Administrateur

class UserFactory:
    """
    DESIGN PATTERN : FACTORY METHOD
    Centralise la création des objets Utilisateurs pour éviter de disperser
    la logique d'instanciation dans toute l'application.
    """

    @staticmethod
    def creer_utilisateur(role: str, data: dict):
        """
        Instancie la bonne sous-classe en fonction du rôle.
        :param role: 'beneficiaire', 'fournisseur' ou 'admin'
        :param data: Dictionnaire contenant les attributs (souvent issu du Repository)
        :return: Une instance de Beneficiaire, Fournisseur ou Administrateur
        """
        role = role.lower()

        # Paramètres communs à tous les utilisateurs
        base_args = {
            "id": data.get('id'),
            "nom": data.get('nom'),
            "email": data.get('email'),
            "mdp": data.get('mot_de_passe')
        }

        if role == "beneficiaire":
            return Beneficiaire(
                **base_args,
                adresse_livraison=data.get('adresse_livraison', ''),
                telephone=data.get('telephone', '')
            )

        elif role == "fournisseur":
            chef = Fournisseur(
                **base_args,
                biographie=data.get('biographie', '')
            )
            # On récupère aussi l'état de validation depuis la DB
            chef.kyc_valide = bool(data.get('kyc_valide', 0))
            chef.solde_accumule = float(data.get('solde', 0.0))
            return chef

        elif role == "admin":
            return Administrateur(**base_args)

        else:
            raise ValueError(f"⚠️ Rôle inconnu : {role}")