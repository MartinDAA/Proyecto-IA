"""Carga del banco de escenarios preconfigurados y del catálogo de pictogramas."""

import json
import os
import random
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ARCHIVO = Path("datos") / "escenarios.json"


@dataclass(frozen=True)
class Pictograma:
    id: str
    nombre: str
    emoji: str
    arasaac: int | None = None
    categoria: str | None = None
    # Secuencia de pictogramas y texto que usa el agente para dar la pista de este elemento.
    pista: tuple[str, ...] = ()
    texto_pista: str = ""


@dataclass(frozen=True)
class Categoria:
    id: str
    nombre: str
    pictograma: str


@dataclass(frozen=True)
class Escenario:
    id: str
    nombre: str
    cielo: str
    objetivo: dict[str, str]
    # Elementos que podrían estar en el lugar: nunca se usan como distractores.
    compatibles: frozenset[str]


@dataclass(frozen=True)
class Banco:
    pictogramas: dict[str, Pictograma]
    categorias: tuple[Categoria, ...]
    escenarios: dict[str, Escenario]

    def categoria(self, id: str) -> Categoria:
        return next(c for c in self.categorias if c.id == id)

    def elementos_de(self, categoria: str) -> list[str]:
        return [p.id for p in self.pictogramas.values() if p.categoria == categoria]

    def distractores(self, escenario: Escenario, categoria: str, rng: random.Random, n: int = 3) -> list[str]:
        """Elige al azar n elementos de la categoría que no pertenecen al escenario."""
        correcto = escenario.objetivo[categoria]
        candidatos = [
            e for e in self.elementos_de(categoria) if e != correcto and e not in escenario.compatibles
        ]
        return rng.sample(candidatos, n)


def ruta_escenarios() -> Path:
    """Ubica datos/escenarios.json subiendo desde este archivo (o usa KITI_ESCENARIOS)."""
    if ruta := os.environ.get("KITI_ESCENARIOS"):
        return Path(ruta)
    for carpeta in Path(__file__).resolve().parents:
        if (carpeta / ARCHIVO).is_file():
            return carpeta / ARCHIVO
    raise FileNotFoundError(f"No se encontró {ARCHIVO}")


@lru_cache
def cargar_banco(ruta: Path | None = None) -> Banco:
    datos = json.loads((ruta or ruta_escenarios()).read_text(encoding="utf-8"))
    pictogramas = {
        id: Pictograma(
            id=id,
            nombre=p["nombre"],
            emoji=p["emoji"],
            arasaac=p.get("arasaac"),
            categoria=p.get("categoria"),
            pista=tuple(p.get("pista", ())),
            texto_pista=p.get("texto_pista", ""),
        )
        for id, p in datos["pictogramas"].items()
    }
    categorias = tuple(Categoria(**c) for c in datos["categorias"])
    escenarios = {
        e["id"]: Escenario(
            id=e["id"],
            nombre=e["nombre"],
            cielo=e["cielo"],
            objetivo=e["objetivo"],
            compatibles=frozenset(e["compatibles"]),
        )
        for e in datos["escenarios"]
    }
    return Banco(pictogramas, categorias, escenarios)
