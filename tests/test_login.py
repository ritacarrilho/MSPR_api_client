import unittest
from unittest.mock import MagicMock, patch
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import Customer 

# Create a TestClient instance
client = TestClient(app)

class TestLogin(unittest.TestCase):

    @patch("app.database.get_db")
    def test_login_success(self, mock_get_db):
        # Mocking a database session and customer
        mock_db = MagicMock()
        mock_customer = Customer(
            id_customer=1,
            created_at="2023-09-23T00:00:00",
            name="John Doe",
            username="johndoe",
            first_name="John",
            last_name="Doe",
            phone="123456789",
            email="test@example.com",
            last_login="2023-09-23T00:00:00",
            customer_type=2,
            failed_login_attempts=0,
            preferred_contact_method=1,
            opt_in_marketing=False,
            loyalty_points=100
        )
        mock_db.query().filter().first.return_value = mock_customer.dict()

        # Mock get_db to return the mock_db session
        mock_get_db.return_value = mock_db

        # Patch the verify_password function to return True for valid password
        with patch("app.middleware.verify_password", return_value=True):
            response = client.post("/login", json={"email": "test@example.com", "password": "password"})
        
        # Assert that the login was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.json())

    @patch("app.database.get_db")  # Mock the get_db dependency
    def test_login_invalid_credentials(self, mock_get_db):
        # Mocking a database session and customer
        mock_db = MagicMock()
        mock_customer = Customer(
            id_customer=1,
            created_at="2023-09-23T00:00:00",
            name="John Doe",
            username="johndoe",
            first_name="John",
            last_name="Doe",
            phone="123456789",
            email="test@example.com",
            last_login="2023-09-23T00:00:00",
            customer_type=2,
            failed_login_attempts=0,
            preferred_contact_method=1,
            opt_in_marketing=False,
            loyalty_points=100
        )
        mock_db.query().filter().first.return_value = mock_customer.dict() 

        # Mock get_db to return the mock_db session
        mock_get_db.return_value = mock_db

        # Patch the verify_password function to return False for invalid credentials
        with patch("app.middleware.verify_password", return_value=False):
            response = client.post("/login", json={"email": "test@example.com", "password": "wrongpassword"})
        
        # Assert that the login failed
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Invalid email or password")

    @patch("app.database.get_db")  # Mock the get_db dependency
    def test_login_customer_not_found(self, mock_get_db):
        # Mocking a database session where no customer is found
        mock_db = MagicMock()
        mock_db.query().filter().first.return_value = None 

        # Mock get_db to return the mock_db session
        mock_get_db.return_value = mock_db

        # Send the request with a non-existing user
        response = client.post("/login", json={"email": "non_existent@example.com", "password": "password"})
        
        # Assert that the login failed due to customer not being found
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Invalid email or password")

# If this file is run directly, run the tests
if __name__ == "__main__":
    unittest.main()
