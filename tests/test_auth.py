import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('app.dependencies.get_user')  # Remplacez par la fonction correcte qui récupère l'utilisateur
    def test_login_success(self, mock_get_user):
        # Simulez le comportement de la fonction de récupération d'utilisateur
        mock_get_user.return_value = {"email": "admin@email.com", "hashed_password": "fake_hashed_password"}

        # Simulez la fonction de vérification du mot de passe
        with patch('app.dependencies.verify_password') as mock_verify_password:
            mock_verify_password.return_value = True  # Le mot de passe est correct

            login_data = {
                "email": "admin@email.com",
                "password": "toto"  # Mettez ici le mot de passe qui correspond à votre logique
            }
            response = self.client.post("/login", json=login_data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {
                "access_token": "mock_token",  # Remplacez par la logique de votre token
                "token_type": "bearer"
            })

    @patch('app.dependencies.get_user')  # Remplacez par la fonction correcte qui récupère l'utilisateur
    def test_login_failure(self, mock_get_user):
        # Simulez l'absence d'utilisateur
        mock_get_user.return_value = None

        login_data = {
            "email": "wrong@email.com",
            "password": "wrong"
        }
        response = self.client.post("/login", json=login_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid credentials"})

    @patch('app.dependencies.get_user')  # Remplacez par la fonction correcte qui récupère l'utilisateur
    def test_login_wrong_password(self, mock_get_user):
        # Simulez le comportement de la fonction de récupération d'utilisateur
        mock_get_user.return_value = {"email": "admin@email.com", "hashed_password": "fake_hashed_password"}

        # Simulez la fonction de vérification du mot de passe
        with patch('app.dependencies.verify_password') as mock_verify_password:
            mock_verify_password.return_value = False  # Le mot de passe est incorrect

            login_data = {
                "email": "admin@email.com",
                "password": "wrong_password"  # Mot de passe incorrect
            }
            response = self.client.post("/login", json=login_data)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {"detail": "Invalid credentials"})

if __name__ == "__main__":
    unittest.main()
