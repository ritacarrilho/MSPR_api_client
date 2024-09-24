import unittest
from unittest.mock import patch
from passlib.context import CryptContext
import os
from jose import jwt, JWTError
from app.middleware import (
    hash_password, verify_password, create_access_token,
    verify_access_token, get_current_customer, is_admin, is_customer_or_admin
)
from fastapi import HTTPException, status


class TestMiddleware(unittest.TestCase):

    @patch.dict(os.environ, {"SECRET_KEY": "secret", "ALGORITHM": "HS256", "ACCESS_TOKEN_EXPIRE_MINUTES": "30"})
    def setUp(self):
        # Mocking the environment variables needed for the JWT functions
        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.ALGORITHM = os.getenv('ALGORITHM')
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

        # Set up CryptContext for password hashing
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Test password hashing
    def test_hash_password(self):
        password = "my_password"
        hashed = hash_password(password)
        self.assertTrue(self.pwd_context.verify(password, hashed))

    # Test password verification
    def test_verify_password(self):
        password = "my_password"
        hashed = hash_password(password)
        result = verify_password(password, hashed)
        self.assertTrue(result)

    # Test password verification with incorrect password
    def test_verify_password_incorrect(self):
        password = "my_password"
        hashed = hash_password("wrong_password")
        result = verify_password(password, hashed)
        self.assertFalse(result)

    # Test JWT token creation
    @patch("app.middleware.jwt.encode", return_value="mock_token")
    def test_create_access_token(self, mock_jwt_encode):
        # Mock JWT encode to simulate token creation
        payload = {"id_customer": 1}
        token = create_access_token(payload)

        # Check that jwt.encode was called with the correct arguments
        mock_jwt_encode.assert_called_once()
        
        # Check the returned token
        self.assertEqual(token, "mock_token")

    # Test JWT token verification (valid)
    @patch("app.middleware.SECRET_KEY", "kawa-microservices-auth")  # Use the correct SECRET_KEY from your app
    @patch("app.middleware.jwt.decode")
    def test_verify_access_token_valid(self, mock_jwt_decode):
        # Mocking JWT decode function
        mock_jwt_decode.return_value = {"id_customer": 1}

        token = "valid_token"
        payload = verify_access_token(token)

        # Ensure jwt.decode was called with the correct arguments
        mock_jwt_decode.assert_called_once_with(token, "kawa-microservices-auth", algorithms=["HS256"])
        
        # Check the returned payload
        self.assertEqual(payload, {"id_customer": 1})

    # Test JWT token verification (invalid)
    @patch("app.middleware.jwt.decode", side_effect=JWTError)
    @patch("app.middleware.SECRET_KEY", "secret")
    def test_verify_access_token_invalid(self, mock_jwt_decode):
        token = "invalid_token"
        payload = verify_access_token(token)

        mock_jwt_decode.assert_called_once_with(token, "secret", algorithms=["HS256"])
        self.assertIsNone(payload)

    # Test get_current_customer (valid token)
    # @patch("app.middleware.oauth2_scheme", return_value="valid_token")  # Mock the oauth2_scheme to return "valid_token"
    # @patch("app.middleware.verify_access_token")
    # def test_get_current_customer_valid(self, mock_verify_access_token, mock_oauth2_scheme):
    #     # Mock verify_access_token to return a valid payload
    #     mock_verify_access_token.return_value = {"id_customer": 1, "customer_type": 2}

    #     # Call the get_current_customer function
    #     result = get_current_customer()

    #     # Ensure verify_access_token was called with the correct token
    #     mock_verify_access_token.assert_called_once_with("valid_token")

    #     # Check that the function returns the expected payload
    #     self.assertEqual(result, {"id_customer": 1, "customer_type": 2})


    # Test get_current_customer (invalid token)
    @patch("app.middleware.verify_access_token")
    @patch("app.middleware.oauth2_scheme", return_value="invalid_token")
    def test_get_current_customer_invalid(self, mock_oauth2_scheme, mock_verify_access_token):
        mock_verify_access_token.return_value = None

        with self.assertRaises(HTTPException) as context:
            get_current_customer()

        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)

    # Test is_admin (valid admin customer)
    def test_is_admin_valid(self):
        current_customer = {"customer_type": 1}
        try:
            is_admin(current_customer)
        except HTTPException:
            self.fail("is_admin() raised HTTPException unexpectedly!")

    # Test is_admin (non-admin customer)
    def test_is_admin_invalid(self):
        current_customer = {"customer_type": 2}

        with self.assertRaises(HTTPException) as context:
            is_admin(current_customer)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)

    # Test is_customer_or_admin (valid customer or admin)
    def test_is_customer_or_admin_valid(self):
        current_customer_admin = {"id_customer": 1, "customer_type": 1}
        current_customer_owner = {"id_customer": 1, "customer_type": 2}
        
        # Admin should pass
        try:
            is_customer_or_admin(current_customer_admin, 2)
        except HTTPException:
            self.fail("is_customer_or_admin() raised HTTPException unexpectedly for admin!")

        # Owner should pass
        try:
            is_customer_or_admin(current_customer_owner, 1)
        except HTTPException:
            self.fail("is_customer_or_admin() raised HTTPException unexpectedly for owner!")

    # Test is_customer_or_admin (invalid customer)
    def test_is_customer_or_admin_invalid(self):
        current_customer = {"id_customer": 1, "customer_type": 2}

        with self.assertRaises(HTTPException) as context:
            is_customer_or_admin(current_customer, 2)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)

if __name__ == '__main__':
    unittest.main()
