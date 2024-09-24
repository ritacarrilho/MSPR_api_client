import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_login_success(self):
        login_data = {
            "email": "admin@email.com",
            "password": "toto"
        }
        response = self.client.post("/login", json=login_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "access_token": "mock_token",
            "token_type": "bearer"
        })

    def test_login_failure(self):
        login_data = {
            "email": "wrong@email.com",
            "password": "wrong"
        }
        response = self.client.post("/login", json=login_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid credentials"})

if __name__ == "__main__":
    unittest.main()
