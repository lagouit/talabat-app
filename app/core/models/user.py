class DocumentKYC:
    def __init__(self, id: int, fournisseur_id: int, type_doc: str, fichier_url: str):
        self.id = id
        self.fournisseur_id = fournisseur_id
        self.type_doc = type_doc # ex: 'CIN' ou 'Passeport'
        self.fichier_url = fichier_url
        self.est_valide = False