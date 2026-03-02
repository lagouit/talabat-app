from app.infrastructure.db.database_manager import DatabaseManager

def main():
    # Test du Singleton
    db1 = DatabaseManager()
    db2 = DatabaseManager()
    
    if db1 is db2:
        print("🚀 Pattern Singleton validé : Les deux instances sont identiques.")
    
    if db1.get_connection():
        print("✅ Base de données prête pour US02.")

if __name__ == "__main__":
    main()