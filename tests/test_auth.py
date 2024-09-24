from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    # Mock des données d'authentification
    login_data = {
        "email": "admin@email.com",
        "password": "toto"
    }
    response = client.post("/login", json=login_data)
    
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "mock_token",
        "token_type": "bearer"
    }

def test_login_failure():
    # Mock des données d'authentification incorrectes
    login_data = {
        "email": "wrong@email.com",
        "password": "wrong"
    }
    response = client.post("/login", json=login_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid credentials"}
