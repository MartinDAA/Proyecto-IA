from fastapi.testclient import TestClient

from app.main import app


def login(client: TestClient, username: str = "admin", password: str = "admin"):
    return client.post("/api/auth/login", json={"username": username, "password": password})


def test_health():
    with TestClient(app) as client:
        assert client.get("/api/health").json() == {"status": "ok"}


def test_login_admin_ok():
    with TestClient(app) as client:
        response = login(client)
        assert response.status_code == 200
        assert response.json()["token_type"] == "bearer"


def test_login_credenciales_incorrectas():
    with TestClient(app) as client:
        assert login(client, password="otra").status_code == 401
        assert login(client, username="nadie").status_code == 401


def test_me_requiere_token():
    with TestClient(app) as client:
        assert client.get("/api/auth/me").status_code == 401
        token = login(client).json()["access_token"]
        response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert response.json()["username"] == "admin"


def auth(client: TestClient) -> dict[str, str]:
    return {"Authorization": f"Bearer {login(client).json()['access_token']}"}


def test_escenarios():
    with TestClient(app) as client:
        assert client.get("/api/escenarios").status_code == 401
        escenarios = client.get("/api/escenarios", headers=auth(client)).json()
        assert len(escenarios) == 10
        assert all(len(e["elementos"]) == 4 for e in escenarios)


def test_iniciar_escenario_inexistente():
    with TestClient(app) as client:
        response = client.post("/api/partida/iniciar", json={"escenario_id": "luna"}, headers=auth(client))
        assert response.status_code == 404


def test_partida_completa_sin_errores():
    with TestClient(app) as client:
        headers = auth(client)
        turno = client.post("/api/partida/iniciar", json={"escenario_id": "granja"}, headers=headers).json()
        assert turno["ronda"] == 1 and len(turno["opciones"]) == 4
        assert turno["mensaje"]["texto"] == "¿Qué animal hay en la granja?"
        correctos = [e["id"] for e in turno["escenario"]["elementos"]]
        for correcto in correctos:
            body = {"partida_id": turno["partida_id"], "pictograma": correcto}
            turno = client.post("/api/partida/responder", json=body, headers=headers).json()
            assert turno["correcto"] is True
        assert turno["terminada"] is True
        assert turno["resumen"]["aciertos_primer_intento"] == 4
        assert turno["resumen"]["estrella"] is True
        assert turno["resumen"]["no_pertenecen"] == []
        body = {"partida_id": turno["partida_id"], "pictograma": "vaca"}
        assert client.post("/api/partida/responder", json=body, headers=headers).status_code == 409


def test_error_da_ayuda_y_retira_la_opcion():
    with TestClient(app) as client:
        headers = auth(client)
        turno = client.post("/api/partida/iniciar", json={"escenario_id": "playa"}, headers=headers).json()
        incorrecto = next(o["id"] for o in turno["opciones"] if o["id"] != "cangrejo")
        body = {"partida_id": turno["partida_id"], "pictograma": incorrecto}
        turno = client.post("/api/partida/responder", json=body, headers=headers).json()
        assert turno["correcto"] is False
        assert turno["ayuda"] is not None
        assert incorrecto not in [o["id"] for o in turno["opciones"]]
        assert turno["retro"]["texto"].endswith("no va aquí.")
        assert turno["ronda"] == 1


def test_partida_de_otro_usuario():
    with TestClient(app) as client:
        body = {"partida_id": "no-existe", "pictograma": "vaca"}
        assert client.post("/api/partida/responder", json=body, headers=auth(client)).status_code == 404
