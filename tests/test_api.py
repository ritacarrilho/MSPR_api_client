import unittest
import subprocess
from sqlalchemy import create_engine, MetaData, Table, insert, select, update, delete, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        # Charger les variables d'environnement
        load_dotenv()
        
        # Récupérer l'URL de la base de données
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise RuntimeError("DATABASE_URL n'est pas définie dans le fichier .env")

        # Connexion à la base de données
        cls.engine = create_engine(database_url)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        cls.metadata = MetaData(bind=cls.engine)
        cls.inspector = inspect(cls.engine)
        
        # Charger les tables nécessaires
        cls.customers_table = Table('Customers', cls.metadata, autoload_with=cls.engine)
        cls.addresses_table = Table('Addresses', cls.metadata, autoload_with=cls.engine)
        cls.companies_table = Table('Companies', cls.metadata, autoload_with=cls.engine)

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    # Test de connexion à la base de données
    def test_database_connection(self):
        """Teste la connexion à la base de données."""
        try:
            connection = self.engine.connect()
            self.assertTrue(connection)
        except SQLAlchemyError as e:
            self.fail(f"Erreur de connexion à la base de données : {e}")
        finally:
            connection.close()

    # Test pour vérifier l'existence de la table 'Customers'
    def test_table_customers_exists(self):
        """Vérifie que la table 'Customers' existe dans test_customer_db."""
        try:
            tables = self.inspector.get_table_names()
            self.assertIn('Customers', tables, "La table 'Customers' n'existe pas dans la base de données.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur SQLAlchemy lors de la vérification de l'existence de la table 'Customers' : {e}")

    # Test pour vérifier l'existence de la table 'Addresses'
    def test_table_addresses_exists(self):
        """Vérifie que la table 'Addresses' existe dans test_customer_db."""
        try:
            tables = self.inspector.get_table_names()
            self.assertIn('Addresses', tables, "La table 'Addresses' n'existe pas dans la base de données.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur SQLAlchemy lors de la vérification de l'existence de la table 'Addresses' : {e}")

    # Test pour vérifier l'existence de la table 'Companies'
    def test_table_companies_exists(self):
        """Vérifie que la table 'Companies' existe dans test_customer_db."""
        try:
            tables = self.inspector.get_table_names()
            self.assertIn('Companies', tables, "La table 'Companies' n'existe pas dans la base de données.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur SQLAlchemy lors de la vérification de l'existence de la table 'Companies' : {e}")

    # Test pour insérer des données dans la table 'Customers'
    def test_insert_into_customers(self):
        """Teste l'insertion d'un client dans la table 'Customers'."""
        try:
            insert_query = insert(self.customers_table).values(
                name="John Doe", email="john.doe@example.com", created_at="2024-09-14 10:00:00"
            )
            result = self.session.execute(insert_query)
            self.session.commit()
            
            # Vérifier que l'insertion a réussi
            self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'Customers' a échoué.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de l'insertion dans 'Customers' : {e}")

    # Test pour insérer des données dans la table 'Addresses'
    def test_insert_into_addresses(self):
        """Teste l'insertion d'une adresse dans la table 'Addresses'."""
        try:
            insert_query = insert(self.addresses_table).values(
                address_line1="123 Rue de Paris", city="Paris", state="Île-de-France", postal_code="75001", country="France", id_customer=1
            )
            result = self.session.execute(insert_query)
            self.session.commit()
            
            # Vérifier que l'insertion a réussi
            self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'Addresses' a échoué.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de l'insertion dans 'Addresses' : {e}")

    # Test pour insérer des données dans la table 'Companies'
    def test_insert_into_companies(self):
        """Teste l'insertion d'une entreprise dans la table 'Companies'."""
        try:
            insert_query = insert(self.companies_table).values(
                name="Tech Corp", address="456 Avenue des Champs-Élysées", email="contact@techcorp.com", phone="0147258369", created_at="2024-09-14 10:00:00"
            )
            result = self.session.execute(insert_query)
            self.session.commit()
            
            # Vérifier que l'insertion a réussi
            self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'Companies' a échoué.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de l'insertion dans 'Companies' : {e}")

    # Test pour lire des données dans la table 'Customers'
    def test_read_from_customers(self):
        """Teste la lecture des données insérées dans la table 'Customers'."""
        try:
            select_query = select([self.customers_table]).where(self.customers_table.c.email == "john.doe@example.com")
            result = self.session.execute(select_query).fetchone()
            
            # Vérifier que les données sont bien récupérées
            self.assertIsNotNone(result, "Aucune donnée trouvée dans la table 'Customers'.")
            self.assertEqual(result['email'], "john.doe@example.com", "Le champ 'email' est incorrect.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la lecture dans 'Customers' : {e}")

    # Test pour mettre à jour des données dans la table 'Customers'
    def test_update_customers(self):
        """Teste la mise à jour d'un client dans la table 'Customers'."""
        try:
            update_query = update(self.customers_table).where(self.customers_table.c.email == "john.doe@example.com").values(name="Jane Doe")
            result = self.session.execute(update_query)
            self.session.commit()

            # Vérifier que la mise à jour a réussi
            self.assertGreater(result.rowcount, 0, "Aucune ligne n'a été mise à jour dans la table 'Customers'.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la mise à jour dans 'Customers' : {e}")

    # Test pour supprimer des données dans la table 'Customers'
    def test_delete_from_customers(self):
        """Teste la suppression d'un client dans la table 'Customers'."""
        try:
            delete_query = delete(self.customers_table).where(self.customers_table.c.email == "john.doe@example.com")
            result = self.session.execute(delete_query)
            self.session.commit()

            # Vérifier que la suppression a réussi
            self.assertGreater(result.rowcount, 0, "Aucune ligne n'a été supprimée dans la table 'Customers'.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la suppression dans 'Customers' : {e}")

    # Test pour lire des données dans la table 'Addresses'
    def test_read_from_addresses(self):
        """Teste la lecture des données insérées dans la table 'Addresses'."""
        try:
            select_query = select([self.addresses_table]).where(self.addresses_table.c.address_line1 == "123 Rue de Paris")
            result = self.session.execute(select_query).fetchone()
            
            # Vérifier que les données sont bien récupérées
            self.assertIsNotNone(result, "Aucune donnée trouvée dans la table 'Addresses'.")
            self.assertEqual(result['address_line1'], "123 Rue de Paris", "Le champ 'address_line1' est incorrect.")
        except SQLAlchemyError as e:
            self.fail(f"Erreur lors de la lecture dans 'Addresses' : {e}")

if __name__ == '__main__':
    unittest.main()
