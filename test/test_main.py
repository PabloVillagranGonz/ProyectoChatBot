from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Credenciales correctas (ajusta según tu fake_users_db)
USERNAME = "usuario1"
PASSWORD = "1234"

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Mensaje": "Bienvenido a la API de ChatBot. Ve a /docs para la documentacion."}

def test_login_correcto():
    response = client.post("/login", data={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_fallido():
    response = client.post("/login", data={"username": "incorrecto", "password": "incorrecto"})
    assert response.status_code == 401

def test_predict():
    # Primero, logueamos para obtener el token
    response = client.post("/login", data={"username": USERNAME, "password": PASSWORD})
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Ahora, hacemos la predicción usando el token
    headers = {"Authorization": f"Bearer {token}"}
    pregunta = {"texto": "¿Qué es una variable en programación?"}
    response = client.post("/predict", json=pregunta, headers=headers)
    assert response.status_code == 200
    assert "texto" in response.json()
    assert "categoria" in response.json()

def test_predict_sin_token():
    pregunta = {"texto": "¿Qué es una variable en programación?"}
    response = client.post("/predict", json=pregunta)
    assert response.status_code == 401
