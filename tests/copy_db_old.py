import mysql.connector
from mysql.connector import Error

def copy_database():
    try:
        # Connexion à la base de données source
        source_conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='customer_db'
        )
        source_cursor = source_conn.cursor()

        # Connexion à la base de données cible
        target_conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password=''
        )
        target_cursor = target_conn.cursor()

        # Supprimer la base de données de test si elle existe
        target_cursor.execute("DROP DATABASE IF EXISTS test_customer_db")
        # Créer la base de données de test
        target_cursor.execute("CREATE DATABASE test_customer_db")
        target_cursor.execute("USE test_customer_db")

        # Récupérer la liste des tables de la base de données source
        source_cursor.execute("SHOW TABLES")
        tables = source_cursor.fetchall()

        # Copier chaque table
        for (table_name,) in tables:
            # Créer la table dans la base de données de test
            source_cursor.execute(f"SHOW CREATE TABLE {table_name}")
            create_table_stmt = source_cursor.fetchone()[1]
            target_cursor.execute(create_table_stmt.replace('customer_db', 'test_customer_db'))

            # Copier les données
            source_cursor.execute(f"SELECT * FROM {table_name}")
            rows = source_cursor.fetchall()
            columns = [desc[0] for desc in source_cursor.description]
            columns_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(columns))
            insert_stmt = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            target_cursor.executemany(insert_stmt, rows)

        # Committer les changements
        target_conn.commit()
        print("La copie de la base de données est terminée.")

    except Error as e:
        print(f"Erreur : {e}")
    
    finally:
        if source_conn.is_connected():
            source_cursor.close()
            source_conn.close()
        if target_conn.is_connected():
            target_cursor.close()
            target_conn.close()

if __name__ == "__main__":
    copy_database()
