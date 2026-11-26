"""Bucle de una partida con un jugador simulado (por defecto, uno que elige al azar)."""

import random
from collections.abc import Callable
from typing import Protocol

from ia_models.agentes import Agente
from ia_models.entorno import CATEGORIAS, Partida, Ronda
from ia_models.escenarios import Banco

Observador = Callable[[str, Partida, dict], None]


class Jugador(Protocol):
    def elegir(self, ronda: Ronda, rng: random.Random) -> str | None: ...


class JugadorAlAzar:
    def elegir(self, ronda: Ronda, rng: random.Random) -> str:
        return rng.choice(ronda.opciones)


def jugar_partida(
    banco: Banco,
    agente: Agente,
    rng: random.Random,
    escenario: str | None = None,
    observar: Observador | None = None,
    jugador: Jugador = JugadorAlAzar(),
) -> Partida:
    e = banco.escenarios[escenario] if escenario else rng.choice(list(banco.escenarios.values()))
    partida = Partida(banco, e, rng=rng)
    for _ in CATEGORIAS:
        ronda = partida.iniciar_ronda()
        if observar:
            observar("ronda", partida, {})
        while True:
            elegido = jugador.elegir(ronda, rng)
            if elegido is None:  # Abandona la ronda: queda sin resolver.
                break
            correcto = partida.responder(elegido)
            if observar:
                observar("respuesta", partida, {"elegido": elegido, "correcto": correcto})
            if correcto:
                break
            ayuda = agente.elegir_ayuda(ronda)
            partida.aplicar_ayuda(ayuda)
            if observar:
                observar("ayuda", partida, {"ayuda": ayuda})
    if observar:
        observar("fin", partida, {})
    return partida
