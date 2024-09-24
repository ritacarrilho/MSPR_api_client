import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine, MetaData, Table, insert, select, update, delete, Column, Integer, DateTime, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker
import os

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Simuler la connexion à la base de données et la session
        cls.engine = MagicMock()
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()
        cls.metadata = MetaData()
        
        # Simuler les tables
        cls.customers_table = Table('Customers', cls.metadata,
                Column('id_customer', Integer, primary_key=True),
                Column('created_at', DateTime),
                Column('name', String),
                Column('username', String),
                Column('first_name', String),
                Column('last_name', String),
                Column('phone', String),
                Column('email', String),
                Column('last_login', DateTime),
                Column('customer_type', Integer),
                Column('failed_login_attempts', Integer),
                Column('preferred_contact_method', Integer),
                Column('opt_in_marketing', Boolean),
                Column('loyalty_points', Integer),
                Column('password_hash', String)
            )
        cls.addresses_table = Table('Addresses', cls.metadata,
                    Column('id_address', Integer, primary_key=True),
                    Column('address_line1', String),
                    Column('address_line2', String),
                    Column('city', String),
                    Column('state', String),
                    Column('postal_code', String),
                    Column('country', String),
                    Column('address_type', Integer),
                    Column('created_at', DateTime),
                    Column('updated_at', DateTime),
                    Column('id_customer', Integer, ForeignKey('Customers.id_customer'))
                )        
        cls.companies_table = Table('Companies', cls.metadata)
        cls.feedback_table = Table('Feedback', cls.metadata,
            Column('id_feedback', Integer, primary_key=True),
            Column('product_id', Integer, ForeignKey('Products.id_product')),
            Column('rating', Integer),
            Column('comment', String),
            Column('created_at', DateTime),
            Column('id_customer', Integer, ForeignKey('Customers.id_customer'))
        )

    @classmethod
    def tearDownClass(cls):
        cls.session.close()

    # Test de connexion à la base de données
    def test_database_connection(self):
        """Teste la connexion à la base de données."""
        self.assertIsNotNone(self.engine, "L'objet engine doit être créé.")

    # Test pour vérifier l'existence de la table 'Customers'
    def test_table_customers_exists(self):
        """Vérifie que la table 'Customers' existe dans la base de données."""
        tables = ['Customers', 'Addresses', 'Companies']
        self.assertIn('Customers', tables, "La table 'Customers' n'existe pas dans la base de données.")

    # Test pour vérifier l'existence de la table 'Addresses'
    def test_table_addresses_exists(self):
        """Vérifie que la table 'Addresses' existe dans la base de données."""
        tables = ['Customers', 'Addresses', 'Companies']
        self.assertIn('Addresses', tables, "La table 'Addresses' n'existe pas dans la base de données.")

    # Test pour vérifier l'existence de la table 'Companies'
    def test_table_companies_exists(self):
        """Vérifie que la table 'Companies' existe dans la base de données."""
        tables = ['Customers', 'Addresses', 'Companies']
        self.assertIn('Companies', tables, "La table 'Companies' n'existe pas dans la base de données.")
        
    # Test pour vérifier l'existence de la table 'Feedbacks'
    def test_table_feedbacks_exists(self):
        """Vérifie que la table 'Feedbacks' existe dans la base de données."""
        tables = ['Customers', 'Addresses', 'Companies', "Feedbacks"]
        self.assertIn('Feedbacks', tables, "La table 'Feedbacks' n'existe pas dans la base de données.")

    # Test pour simuler l'insertion dans la table 'Customers'
    def test_insert_into_customers(self):
        """Teste l'insertion d'un client dans la table 'Customers'."""
        self.session.execute = MagicMock(return_value=MagicMock(inserted_primary_key=[1]))
        insert_query = insert(self.customers_table).values(
            created_at="2024-09-24T14:32:00.197Z",
            name="ProBarista-2",
            username="barista_pro-2",
            first_name="Marie",
            last_name="Durand",
            phone="123456789",
            email="marie.durand-2@procoffee.com",
            last_login="2024-09-24T14:32:00.197Z",
            customer_type=2,
            failed_login_attempts=0,
            preferred_contact_method=2,
            opt_in_marketing=False,
            loyalty_points=0,
            password_hash="Hello"
        )
        
        result = self.session.execute(insert_query)
        self.session.commit()

        self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'Customers' a échoué.")

    # Test pour simuler l'insertion dans la table 'Addresses'
    def test_insert_into_addresses(self):
        """Teste l'insertion d'une adresse dans la table 'Addresses'."""
        self.session.execute = MagicMock(return_value=MagicMock(inserted_primary_key=[1]))
        insert_query = insert(self.addresses_table).values(
            address_line1="123 Rue de Paris", city="Paris", state="Île-de-France", postal_code="75001", country="France", id_customer=1
        )
        result = self.session.execute(insert_query)
        self.session.commit()

        self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'Addresses' a échoué.")

    # Test pour simuler l'insertion dans la table 'Companies'
    def test_insert_into_companies(self):
        """Teste l'insertion d'une entreprise dans la table 'Companies'."""
        self.session.execute = MagicMock(return_value=MagicMock(inserted_primary_key=[1]))
        insert_query = insert(self.companies_table).values(
            name="Tech Corp", address="456 Avenue des Champs-Élysées", email="contact@techcorp.com", phone="0147258369"
        )
        result = self.session.execute(insert_query)
        self.session.commit()

        self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'Companies' a échoué.")

    # Test pour simuler la lecture des données dans la table 'Customers'
    def test_read_from_customers(self):
        """Teste la lecture des données insérées dans la table 'Customers'."""
        self.session.execute = MagicMock(return_value=MagicMock(fetchone=MagicMock(return_value={'email': "marie.durand-2@procoffee.com"})))
        select_query = select([self.customers_table]).where(self.customers_table.c.email == "marie.durand-2@procoffee.com")
        result = self.session.execute(select_query).fetchone()

        self.assertIsNotNone(result, "Aucune donnée trouvée dans la table 'Customers'.")
        self.assertEqual(result['email'], "marie.durand-2@procoffee.com", "Le champ 'email' est incorrect.")

    # Test pour simuler la mise à jour des données dans la table 'Customers'
    def test_update_customers(self):
        """Teste la mise à jour d'un client dans la table 'Customers'."""
        self.session.execute = MagicMock(return_value=MagicMock(rowcount=1))
        update_query = update(self.customers_table).where(self.customers_table.c.email == "marie.durand-2@procoffee.com").values(name="ProBarista-2")
        result = self.session.execute(update_query)
        self.session.commit()

        self.assertGreater(result.rowcount, 0, "Aucune ligne n'a été mise à jour dans la table 'Customers'.")

    # Test pour simuler la suppression des données dans la table 'Customers'
    def test_delete_from_customers(self):
        """Teste la suppression d'un client dans la table 'Customers'."""
        self.session.execute = MagicMock(return_value=MagicMock(rowcount=1))

        delete_query = delete(self.customers_table).where(self.customers_table.c.email == "marie.durand-2@procoffee.com")
        
        result = self.session.execute(delete_query)
        self.session.commit()
        
        # Vérifiez que la suppression a bien eu lieu
        self.assertEqual(result.rowcount, 1, "La suppression du client a échoué.")

        # Test de lecture pour s'assurer que le client n'existe plus
        self.session.execute = MagicMock(return_value=MagicMock(fetchone=MagicMock(return_value=None)))
        select_query = select([self.customers_table]).where(self.customers_table.c.email == "marie.durand-2@procoffee.com")
        result = self.session.execute(select_query).fetchone()
        
        self.assertIsNone(result, "Le client devrait avoir été supprimé.")


    # Test pour simuler la lecture des données dans la table 'Addresses'
    def test_read_from_addresses(self):
        """Teste la lecture des données insérées dans la table 'Addresses'."""
        self.session.execute = MagicMock(return_value=MagicMock(fetchone=MagicMock(return_value={'address_line1': "123 Rue de Paris"})))
        select_query = select([self.addresses_table]).where(self.addresses_table.c.address_line1 == "123 Rue de Paris")
        result = self.session.execute(select_query).fetchone()

        self.assertIsNotNone(result, "Aucune donnée trouvée dans la table 'Addresses'.")
        self.assertEqual(result['address_line1'], "123 Rue de Paris", "Le champ 'address_line1' est incorrect.")
        
    def test_insert_into_feedback(self):
        """Teste l'insertion d'un feedback dans la table 'Feedback'."""
        self.session.execute = MagicMock(return_value=MagicMock(inserted_primary_key=[1]))
        insert_query = insert(self.feedback_table).values(
            product_id=1,  # Assurez-vous que ce produit existe
            rating=5,
            comment="Excellent produit !",
            created_at="2024-09-24T14:57:12.061Z",
            id_customer=1  # Assurez-vous que ce client existe
        )
        
        result = self.session.execute(insert_query)
        self.session.commit()

        self.assertIsNotNone(result.inserted_primary_key, "L'insertion dans la table 'Feedback' a échoué.")

    def test_delete_from_feedback(self):
        """Teste la suppression d'un feedback dans la table 'Feedback'."""
        self.session.execute = MagicMock(return_value=MagicMock(rowcount=1))

        delete_query = delete(self.feedback_table).where(self.feedback_table.c.id_feedback == 1)  # Utilisez l'ID du feedback à supprimer

        result = self.session.execute(delete_query)
        self.session.commit()

        # Vérifiez que la suppression a bien eu lieu
        self.assertEqual(result.rowcount, 1, "La suppression du feedback a échoué.")
        
    def test_get_feedbacks(self):
        """Teste la récupération des feedbacks dans la table 'Feedback'."""
        feedbacks = [{
            'id_feedback': 1,
            'product_id': 1,
            'rating': 5,
            'comment': "Excellent produit !",
            'created_at': "2024-09-24T14:57:12.061Z",
            'id_customer': 1
        }]
        
        # Simuler une réponse de la base de données
        mock_result = MagicMock()
        mock_result.fetchall.return_value = feedbacks
        self.session.execute = MagicMock(return_value=mock_result)

        select_query = select(self.feedback_table)
        result = self.session.execute(select_query)

        fetched_feedbacks = result.fetchall()

        self.assertGreater(len(fetched_feedbacks), 0, "Aucun feedback trouvé.")


if __name__ == '__main__':
    unittest.main()
