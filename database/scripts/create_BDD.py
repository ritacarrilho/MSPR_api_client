import mysql.connector
from mysql.connector import errorcode
import json
import os

# Informations de connexion MySQL
config = {
    'user': 'root',      
    'password': '',      
    'host': 'localhost', 
}

# Nom de la base de données
db_name = 'customer_bd'

# Chemin fichier data
json_file_path = os.path.join('data', 'data.json')

# Connexion à MySQL
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Suppression de la base de données si elle existe déjà
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")
        print(f"La base de données '{db_name}' a été supprimée.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la suppression de la base de données : {err}")

    # Création de la base de données
    try:
        cursor.execute(f"CREATE DATABASE {db_name} DEFAULT CHARACTER SET 'utf8'")
        print(f"La base de données '{db_name}' a été créée avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur lors de la création de la base de données : {err}")
        if err.errno == errorcode.ER_DB_CREATE_EXISTS:
            print(f"La base de données '{db_name}' existe déjà.")
        else:
            print(err)

    # Sélectionner la base de données
    cursor.execute(f"USE {db_name}")

    # Définir les requêtes de création des tables
    create_tables_queries = {
        'Customers': """
            CREATE TABLE Customers (
                id_customer VARCHAR(50),
                created_at DATETIME NOT NULL,
                name VARCHAR(80) NOT NULL,
                username VARCHAR(80) NOT NULL,
                first_name VARCHAR(80) NOT NULL,
                last_name VARCHAR(80) NOT NULL,
                postal_code VARCHAR(10) NOT NULL,
                city VARCHAR(90) NOT NULL,
                PRIMARY KEY (id_customer)
            )
        """,
        'Companies': """
            CREATE TABLE companies (
                id_customer VARCHAR(50),
                id_company VARCHAR(80),
                company_name VARCHAR(80) NOT NULL,
                PRIMARY KEY (id_customer, id_company),
                FOREIGN KEY (id_customer) REFERENCES Customers(id_customer)
            )
        """,
        'Orders': """
            CREATE TABLE orders (
                id_customer VARCHAR(50),
                id_order VARCHAR(80),
                created_at DATETIME NOT NULL,
                PRIMARY KEY (id_customer, id_order),
                FOREIGN KEY (id_customer) REFERENCES Customers(id_customer)
            )
        """,
        'Profiles': """
            CREATE TABLE profiles (
                id_profile VARCHAR(80),
                first_name VARCHAR(80) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                id_customer VARCHAR(50) NOT NULL,
                PRIMARY KEY (id_profile),
                FOREIGN KEY (id_customer) REFERENCES Customers(id_customer)
            )
        """
    }

    # Création des tables
    for table_name, create_query in create_tables_queries.items():
        try:
            cursor.execute(create_query)
            print(f"Table '{table_name}' créée avec succès.")
        except mysql.connector.Error as err:
            print(f"Erreur lors de la création de la table {table_name} : {err}")

    # Fermer la connexion
    cursor.close()
    cnx.close()

except mysql.connector.Error as err:
    print(f"Erreur de connexion à MySQL : {err}")