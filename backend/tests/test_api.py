from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        assert client.get("/api/health").json() == {"status": "ok"}


def test_escenarios():
    with TestClient(app) as client:
        escenarios = client.get("/api/escenarios").json()
        assert len(escenarios) == 10
        assert all(len(e["elementos"]) == 4 for e in escenarios)


def test_iniciar_escenario_inexistente():
    with TestClient(app) as client:
        response = client.post("/api/partida/iniciar", json={"escenario_id": "luna"})
        assert response.status_code == 404


def test_partida_completa_sin_errores():
    with TestClient(app) as client:
        turno = client.post("/api/partida/iniciar", json={"escenario_id": "granja"}).json()
        assert turno["ronda"] == 1 and len(turno["opciones"]) == 4
        assert turno["mensaje"]["texto"] == "¿Qué animal hay en la granja?"
        correctos = [e["id"] for e in turno["escenario"]["elementos"]]
        for correcto in correctos:
            body = {"partida_id": turno["partida_id"], "pictograma": correcto}
            turno = client.post("/api/partida/responder", json=body).json()
            assert turno["correcto"] is True
        assert turno["terminada"] is True
        assert turno["resumen"]["aciertos_primer_intento"] == 4
        assert turno["resumen"]["estrella"] is True
        assert turno["resumen"]["no_pertenecen"] == []
        body = {"partida_id": turno["partida_id"], "pictograma": "vaca"}
        assert client.post("/api/partida/responder", json=body).status_code == 409


def test_error_da_ayuda_y_retira_la_opcion():
    with TestClient(app) as client:
        turno = client.post("/api/partida/iniciar", json={"escenario_id": "playa"}).json()
        incorrecto = next(o["id"] for o in turno["opciones"] if o["id"] != "cangrejo")
        body = {"partida_id": turno["partida_id"], "pictograma": incorrecto}
        turno = client.post("/api/partida/responder", json=body).json()
        assert turno["correcto"] is False
        assert turno["ayuda"] is not None
        assert incorrecto not in [o["id"] for o in turno["opciones"]]
        assert turno["retro"]["texto"].endswith("no va aquí.")
        assert turno["ronda"] == 1


def test_partida_inexistente():
    with TestClient(app) as client:
        body = {"partida_id": "no-existe", "pictograma": "vaca"}
        assert client.post("/api/partida/responder", json=body).status_code == 404


def test_perfiles():
    with TestClient(app) as client:
        perfiles = client.get("/api/perfiles").json()
        assert "estandar" in [p["id"] for p in perfiles]


def test_la_ayuda_depende_del_perfil():
    with TestClient(app) as client:
        primera = {}
        for perfil in ("baja_tolerancia", "autonomia"):
            body = {"escenario_id": "granja", "perfil": perfil}
            turno = client.post("/api/partida/iniciar", json=body).json()
            # Hasta la ronda de transporte, donde las tablas de ambos perfiles difieren.
            for correcto in ("vaca", "granero"):
                body = {"partida_id": turno["partida_id"], "pictograma": correcto}
                turno = client.post("/api/partida/responder", json=body).json()
            body["pictograma"] = next(o["id"] for o in turno["opciones"] if o["id"] != "tractor")
            turno = client.post("/api/partida/responder", json=body).json()
            primera[perfil] = turno["ayuda"]["accion"]
        assert primera["baja_tolerancia"] == "modelar"
        assert primera["autonomia"] != "modelar"


def test_perfil_inexistente():
    with TestClient(app) as client:
        body = {"escenario_id": "granja", "perfil": "otro"}
        assert client.post("/api/partida/iniciar", json=body).status_code == 404


def test_evitar_elementos():
    with TestClient(app) as client:

        def iniciar(evitar: list[str]):
            body = {"escenario_id": "granja", "evitar": evitar}
            return client.post("/api/partida/iniciar", json=body)

        for _ in range(20):
            opciones = [o["id"] for o in iniciar(["mono", "rana", "camello"]).json()["opciones"]]
            assert len(opciones) == 4 and not {"mono", "rana", "camello"} & set(opciones)
        # El paisaje muestra un elemento a evitar, o no quedan distractores (aunque sea en otra ronda).
        assert iniciar(["vaca"]).status_code == 409
        assert iniciar(["semaforo", "ancla", "cactus", "totora", "platano", "sombrilla", "copo_nieve"]).status_code == 409
