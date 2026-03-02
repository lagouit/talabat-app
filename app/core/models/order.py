class Evaluation:
    def __init__(self, id: int, commande_id: int, note: int, commentaire: str):
        if not (1 <= note <= 5):
            raise ValueError("La note doit être comprise entre 1 et 5.")
        self.id = id
        self.commande_id = commande_id
        self.note = note
        self.commentaire = commentaire
        self.date_evaluation = datetime.now()