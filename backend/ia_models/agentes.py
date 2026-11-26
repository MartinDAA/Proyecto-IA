"""Agentes que eligen la ayuda tras cada error."""

import json
from pathlib import Path
from typing import Protocol

from ia_models.entorno import CATEGORIAS, Ayuda, Ronda

POLITICAS = Path(__file__).resolve().parents[1] / "datos" / "politicas.json"

# Orden fijo de ayudas: de la más leve a la que muestra la respuesta.
GUION = (Ayuda.RESALTAR, Ayuda.PISTA, Ayuda.MODELAR)


class Agente(Protocol):
    nombre: str

    def elegir_ayuda(self, ronda: Ronda) -> Ayuda: ...


class AgenteProgramado:
    """Tras cada error da la siguiente ayuda del guion, igual para todas las categorías."""

    nombre = "programado"

    def elegir_ayuda(self, ronda: Ronda) -> Ayuda:
        # Con 4 opciones hay como máximo 3 errores, así que el guion siempre alcanza.
        return GUION[min(len(ronda.ayudas), len(GUION) - 1)]


class AgenteGenetico:
    """Sigue la tabla categoría × error que el algoritmo genético calculó para un perfil.

    La tabla es fija: no cambia durante la partida, para que el juego sea predecible.
    """

    nombre = "genetico"

    def __init__(self, politica: dict[str, tuple[Ayuda, ...]]) -> None:
        self.politica = politica

    def elegir_ayuda(self, ronda: Ronda) -> Ayuda:
        fila = self.politica[ronda.categoria]
        return fila[min(len(ronda.ayudas), len(fila) - 1)]


def cargar_agentes() -> dict[str, AgenteGenetico]:
    """Un agente por perfil, desde datos/politicas.json (lo escribe entrenar_politicas.py)."""
    datos = json.loads(POLITICAS.read_text(encoding="utf-8"))
    return {
        perfil: AgenteGenetico({c: tuple(Ayuda[a.upper()] for a in d["politica"][c]) for c in CATEGORIAS})
        for perfil, d in datos.items()
    }
