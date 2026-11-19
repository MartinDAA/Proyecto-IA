"""Bucle de una partida con un jugador simulado que elige al azar entre las opciones visibles."""

import random
from collections.abc import Callable

from ia_models.agentes import AgenteProgramado
from ia_models.entorno import CATEGORIAS, Partida
from ia_models.escenarios import Banco

Observador = Callable[[str, Partida, dict], None]


def jugar_partida(
    banco: Banco,
    agente: AgenteProgramado,
    rng: random.Random,
    escenario: str | None = None,
    observar: Observador | None = None,
) -> Partida:
    e = banco.escenarios[escenario] if escenario else rng.choice(list(banco.escenarios.values()))
    partida = Partida(banco, e, rng=rng)
    for _ in CATEGORIAS:
        ronda = partida.iniciar_ronda()
        if observar:
            observar("ronda", partida, {})
        while True:
            elegido = rng.choice(ronda.opciones)
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
