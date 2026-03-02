class DocumentKYC:
    def __init__(self, id: int, fournisseur_id: int, type_doc: str, fichier_url: str):
        self.id = id
        self.fournisseur_id = fournisseur_id
        self.type_doc = type_doc # ex: 'CIN' ou 'Passeport'
        self.fichier_url = fichier_url
        self.est_valide = False
from abc import ABC, abstractmethod

class Utilisateur(ABC):
    def __init__(self, id: int, nom: str, email: str, mot_de_passe: str):
        self._id = id                 # Protégé
        self.nom = nom               # Public
        self.email = email           # Public
        self.__mot_de_passe = mot_de_passe # Privé (Encapsulation)

    def get_mot_de_passe(self):
        return self.__mot_de_passe
        # ... (code précédent)
    def modifier_solde(self, montant: float):
        """LSP : Toutes les sous-classes acceptent cette opération de base"""
        # Logique de base commune
        pass

class Beneficiaire(Utilisateur):
    def __init__(self, id, nom, email, mdp, adresse_livraison: str, telephone: str):
        super().__init__(id, nom, email, mdp)
        self.adresse_livraison = adresse_livraison
        self.telephone = telephone

class Fournisseur(Utilisateur):
    def __init__(self, id, nom, email, mdp, biographie: str):
        super().__init__(id, nom, email, mdp)
        self.biographie = biographie
        self.kyc_valide = False
        self.solde_accumule = 0.0
        # ... (code précédent)
    def modifier_solde(self, montant: float):
        """Spécialisation sans briser le contrat de la classe mère"""
        self.solde_accumule += montant
