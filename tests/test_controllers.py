import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.controllers import (
    get_customers, get_customer_by_id, create_customer, update_customer, delete_customer
)
from app.models import Customer
from app.schemas import CustomerCreate, CustomerUpdate
from datetime import datetime

class TestCustomerController(unittest.TestCase):

    def setUp(self):
        # Set up a mock database session for each test
        self.db = MagicMock(spec=Session)

    # def test_get_customers(self):
    #     # Create mock customers
    #     mock_customers = [Customer(id_customer=1, name="John Doe"), Customer(id_customer=2, name="Jane Doe")]
    #     self.db.query().all.return_value = mock_customers

    #     # Call the get_customers function
    #     result = get_customers(self.db)

    #     # Assert that the returned result is correct
    #     self.db.query.assert_called_once_with(Customer)
    #     self.assertEqual(len(result), 2)
    #     self.assertEqual(result[0].name, "John Doe")
    #     self.assertEqual(result[1].name, "Jane Doe")

    def test_get_customer_by_id_found(self):
        # Create a mock customer
        mock_customer = Customer(id_customer=1, name="John Doe")
        self.db.query().filter().first.return_value = mock_customer

        # Call the function
        result = get_customer_by_id(self.db, 1)

        # Assert the query was called correctly and the result is as expected
        self.db.query().filter().first.assert_called_once()
        self.assertEqual(result.name, "John Doe")

    def test_get_customer_by_id_not_found(self):
        # Simulate a missing customer
        self.db.query().filter().first.return_value = None

        # Call the function
        result = get_customer_by_id(self.db, 999)

        # Assert that None is returned
        self.assertIsNone(result)

    @patch("app.controllers.hash_password")
    def test_create_customer(self, mock_hash_password):
        # Mock hash_password function
        mock_hash_password.return_value = "hashed_password"

        # Mock CustomerCreate input
        customer_create = CustomerCreate(
            name="John Doe",
            created_at=datetime.now(),
            username="johndoe",
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="johndoe@example.com",
            password_hash="password123",
            last_login=datetime.now(),
            customer_type=2,
            failed_login_attempts=0,
            preferred_contact_method=1,
            opt_in_marketing=True,
            loyalty_points=100
        )

        # Call the create_customer function
        result = create_customer(self.db, customer_create)

        # Assert that the session's methods were called correctly
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        # Assert the customer password was hashed
        mock_hash_password.assert_called_once_with("password123")

    def test_update_customer(self):
        # Create a mock customer and mock the get_customer_by_id function
        mock_customer = Customer(id_customer=1, name="John Doe")
        self.db.query().filter().first.return_value = mock_customer

        # Mock CustomerUpdate input
        customer_update = CustomerUpdate(first_name="John Updated", loyalty_points=150)

        # Call the update_customer function
        result = update_customer(self.db, 1, customer_update)

        # Assert the customer was updated and committed
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        # Verify that the customer was updated correctly
        self.assertEqual(result.first_name, "John Updated")
        self.assertEqual(result.loyalty_points, 150)

    def test_delete_customer(self):
        # Create a mock customer
        mock_customer = Customer(id_customer=1, name="John Doe")
        self.db.query().filter().first.return_value = mock_customer

        # Call the delete_customer function
        result = delete_customer(self.db, 1)

        # Assert the customer was deleted and committed
        self.db.delete.assert_called_once_with(mock_customer)
        self.db.commit.assert_called_once()

        # Assert that the result is the deleted customer
        self.assertEqual(result.name, "John Doe")

    def test_delete_customer_not_found(self):
        # Simulate customer not found
        self.db.query().filter().first.return_value = None

        # Call the delete_customer function
        result = delete_customer(self.db, 999)

        # Assert that delete was never called
        self.db.delete.assert_not_called()
        self.db.commit.assert_not_called()

        # Assert the result is None
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()