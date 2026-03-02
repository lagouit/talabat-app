def afficher_stats_plateforme(admin_service):
    stats = admin_service.repo.obtenir_stats_ventes()
    print("\n--- 📊 TABLEAU DE BORD GLOBAL ---")
    print(f"✅ Commandes clôturées : {stats['total_commandes']}")
    print(f"💰 Chiffre d'affaires total : {stats['chiffre_affaires']} DH")
    print(f"📈 Panier moyen : {stats['panier_moyen']:.2f} DH")
    print("---------------------------------")