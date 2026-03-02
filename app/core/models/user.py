from abc import ABC, abstractmethod

class Utilisateur(ABC):
    """
    Classe Abstraite (Domaine)
    Représente la base de tout utilisateur du système Talabat.
    """
    def _init_(self, id: int, nom: str, email: str, mot_de_passe: str):
        self._id = id                 # Attribut protégé (Accessible par les sous-classes)
        self.nom = nom               # Attribut public
        self.email = email           # Attribut public
        self.__mot_de_passe = mot_de_passe # Attribut privé (Encapsulation stricte)
        self.est_actif = True

    # Getter pour le mot de passe (Encapsulation)
    def get_password(self) -> str:
        return self.__mot_de_passe

    # Setter pour le mot de passe (si besoin de modification)
    def set_password(self, nouveau_mdp: str):
        if len(nouveau_mdp) >= 8:
            self.__mot_de_passe = nouveau_mdp
        else:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères.")

    @abstractmethod
    def afficher_profil(self):
        """Méthode abstraite imposant une implémentation aux sous-classes"""
        pass

class Beneficiaire(Utilisateur):
    """
    Entité Client (Bénéficiaire)
    """
    def _init_(self, id, nom, email, mdp, adresse_livraison: str, telephone: str):
        super()._init_(id, nom, email, mdp)
        self.adresse_livraison = adresse_livraison
        self.telephone = telephone
        self.solde = 0.0

    def afficher_profil(self):
        return f"[Client] {self.nom} - Livraison à : {self.adresse_livraison}"

class Fournisseur(Utilisateur):
    """
    Entité Chef (Fournisseur)
    """
    def _init_(self, id, nom, email, mdp, biographie: str):
        super()._init_(id, nom, email, mdp)
        self.biographie = biographie
        self.kyc_valide = False      # Statut de validation admin
        self.solde_accumule = 0.0    # Argent gagné (libéré du séquestre)

    def afficher_profil(self):
        statut = "Validé" if self.kyc_valide else "En attente de validation"
        return f"[Chef] {self.nom} - Statut : {statut}"

class Administrateur(Utilisateur):
    """
    Entité Admin
    """
    def _init_(self, id, nom, email, mdp):
        super()._init_(id, nom, email, mdp)
        self.niveau_acces = "SuperAdmin"

    def afficher_profil(self):
        return f"[Admin] {self.nom} (Accès : {self.niveau_acces})"