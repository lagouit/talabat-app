# À ajouter dans OrderRepository
def modifier_statut(self, order_id: int, nouveau_statut: str) -> bool:
    cursor = self.__db.cursor()
    query = "UPDATE commandes SET statut = %s WHERE id = %s"
    try:
        cursor.execute(query, (nouveau_statut, order_id))
        self.__db.commit()
        return True
    except Exception as e:
        print(f"❌ Erreur SQL changement statut : {e}")
        return False