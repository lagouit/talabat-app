def obtenir_stats_ventes(self):
    """Requête SQL agrégée (SUM, COUNT)"""
    cursor = self.__db.cursor(dictionary=True)
    query = """
        SELECT 
            COUNT(id) as total_commandes,
            SUM(montant_total) as chiffre_affaires,
            AVG(montant_total) as panier_moyen
        FROM commandes 
        WHERE statut = 'CONFIRME'
    """
    cursor.execute(query)
    return cursor.fetchone()

def enregistrer_note(self, commande_id: int, note: int, commentaire: str):
    cursor = self.__db.cursor()
    query = "INSERT INTO evaluations (commande_id, note, commentaire) VALUES (%s, %s, %s)"
    cursor.execute(query, (commande_id, note, commentaire))
    self.__db.commit()