# À ajouter dans OrderRepository
def executer_sequestre(self, client_id: int, montant: float, commande_id: int) -> bool:
    cursor = self.__db.cursor()
    try:
        self.__db.start_transaction()
        
        # 1. Vérification et débit du solde client
        cursor.execute("UPDATE utilisateurs SET solde = solde - %s WHERE id = %s AND solde >= %s", 
                       (montant, client_id, montant))
        
        if cursor.rowcount == 0:
            raise Exception("Solde insuffisant")

        # 2. Création de l'enregistrement de séquestre
        query = "INSERT INTO paiements_sequestre (commande_id, montant, statut) VALUES (%s, %s, 'BLOQUE')"
        cursor.execute(query, (commande_id, montant))
        
        self.__db.commit()
        return True
    except Exception as e:
        self.__db.rollback()
        print(f"❌ Échec séquestre : {e}")
        return False