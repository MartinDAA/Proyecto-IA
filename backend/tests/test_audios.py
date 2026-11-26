"""Cada frase que el juego dice en voz alta tiene su audio pregrabado (generar_audios.py)."""

import json
import random

from fastapi.testclient import TestClient

from app.main import app
from ia_models.escenarios import cargar_banco
from ia_models.herramientas import descargar_pictogramas
from ia_models.herramientas.generar_audios import INDICE, SALIDA


def test_partidas_simuladas_tienen_audio():
    indice = json.loads(INDICE.read_text(encoding="utf-8"))
    assert all((SALIDA / archivo).is_file() for archivo in indice.values())
    rng = random.Random(0)
    dichos: set[str] = set()
    with TestClient(app) as client:
        for escenario in cargar_banco().escenarios:
            for _ in range(3):
                turno = client.post("/api/partida/iniciar", json={"escenario_id": escenario}).json()
                while True:
                    dichos.add(turno["mensaje"]["texto"])
                    if turno["retro"]:
                        dichos.add(turno["retro"]["texto"])
                    if turno["terminada"]:
                        dichos |= {m["texto"] for m in turno["resumen"]["no_pertenecen"]}
                        break
                    body = {"partida_id": turno["partida_id"], "pictograma": rng.choice(turno["opciones"])["id"]}
                    turno = client.post("/api/partida/responder", json=body).json()
    assert dichos - indice.keys() == set()


def test_pictogramas_guardados():
    """Si falla tras agregar pictogramas: volver a ejecutar descargar_pictogramas."""
    faltan = [i for i in descargar_pictogramas.identificadores() if not (descargar_pictogramas.SALIDA / f"{i}.webp").is_file()]
    assert faltan == []
