"""Modelo del jugador simulado y valor de una política de ayudas para cada perfil.

shortcut: las probabilidades y los pesos son supuestos del equipo, calibrarlos con la especialista.
"""

import random
from dataclasses import dataclass

from ia_models.entorno import CATEGORIAS, Ayuda, Ronda

N_OPCIONES = 4
ACIERTO_SIN_AYUDA = 0.35
REPETIR_AYUDA = 0.6  # Repetir la misma ayuda rinde un 40 % menos.
PROB_ACIERTO = {
    "animal": {Ayuda.RESALTAR: 0.55, Ayuda.PISTA: 0.70, Ayuda.MODELAR: 1.0},
    "construccion": {Ayuda.RESALTAR: 0.65, Ayuda.PISTA: 0.45, Ayuda.MODELAR: 1.0},
    "transporte": {Ayuda.RESALTAR: 0.50, Ayuda.PISTA: 0.50, Ayuda.MODELAR: 1.0},
    "objeto": {Ayuda.RESALTAR: 0.35, Ayuda.PISTA: 0.30, Ayuda.MODELAR: 1.0},
}

Politica = dict[str, tuple[Ayuda, ...]]


@dataclass(frozen=True)
class Perfil:
    id: str
    nombre: str
    descripcion: str
    # Probabilidad de abandonar tras el error k: frustracion · k (modelar la evita).
    frustracion: float = 0.22
    premio: float = 10
    premio_modelado: float = 3
    costo_error: float = 2
    costo_abandono: float = 6

    def prob_abandono(self, errores: int, ultima: Ayuda | None) -> float:
        if ultima is None or ultima == Ayuda.MODELAR:
            return 0
        return min(1, self.frustracion * errores)

    def puntaje(self, ronda: Ronda) -> float:
        if not ronda.resuelta:
            return -self.costo_abandono
        premio = self.premio_modelado if Ayuda.MODELAR in ronda.ayudas else self.premio
        return premio - self.costo_error * ronda.errores


PERFILES = {
    p.id: p
    for p in (
        Perfil("baja_tolerancia", "Se frustra con facilidad", "Muestra antes la respuesta para evitar el malestar.",
               frustracion=0.30),
        Perfil("estandar", "Estándar", "Equilibra la ayuda y el intento propio."),
        Perfil("autonomia", "Autonomía", "Da más oportunidades antes de mostrar la respuesta.",
               frustracion=0.15),
    )
}


def prob_acierto(categoria: str, ayudas: list[Ayuda] | tuple[Ayuda, ...]) -> float:
    """Probabilidad de acertar el siguiente intento: hubo un error por cada ayuda recibida."""
    restantes = N_OPCIONES - len(ayudas)
    if restantes <= 1:
        return 1
    if not ayudas:
        return ACIERTO_SIN_AYUDA
    ultima = ayudas[-1]
    p = PROB_ACIERTO[categoria][ultima]
    if ultima != Ayuda.MODELAR and ultima in ayudas[:-1]:
        p *= REPETIR_AYUDA
    return max(p, 1 / restantes)


def valor_ronda(perfil: Perfil, categoria: str, fila: tuple[Ayuda, ...]) -> float:
    """Puntaje esperado de una ronda (exacto, sin simular)."""

    def esperado(errores: int) -> float:
        ayudas = fila[:errores]
        premio = perfil.premio_modelado if Ayuda.MODELAR in ayudas else perfil.premio
        logro = premio - perfil.costo_error * errores
        p = prob_acierto(categoria, ayudas)
        if p >= 1:
            return logro
        a = perfil.prob_abandono(errores + 1, fila[errores])
        return p * logro + (1 - p) * (a * -perfil.costo_abandono + (1 - a) * esperado(errores + 1))

    return esperado(0)


def valor(perfil: Perfil, politica: Politica) -> float:
    """Aptitud de la política: puntaje esperado de la partida completa."""
    return sum(valor_ronda(perfil, c, politica[c]) for c in CATEGORIAS)


class JugadorSimulado:
    """Elige según el modelo anterior; devuelve None si abandona la ronda."""

    def __init__(self, perfil: Perfil) -> None:
        self.perfil = perfil

    def elegir(self, ronda: Ronda, rng: random.Random) -> str | None:
        ultima = ronda.ayudas[-1] if ronda.ayudas else None
        if rng.random() < self.perfil.prob_abandono(ronda.errores, ultima):
            return None
        if rng.random() < prob_acierto(ronda.categoria, ronda.ayudas):
            return ronda.correcto
        return rng.choice([o for o in ronda.opciones if o != ronda.correcto])
