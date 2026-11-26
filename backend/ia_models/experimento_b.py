"""Experimento B: agente programado contra agente genético, con el jugador simulado de cada perfil.

Uso (desde backend/):
    uv run python -m ia_models.experimento_b
    uv run python -m ia_models.experimento_b --partidas 5000 --semilla 7
"""

import argparse
import random
from statistics import mean

from ia_models.agentes import AgenteProgramado, cargar_agentes
from ia_models.entorno import Ayuda
from ia_models.escenarios import cargar_banco
from ia_models.jugador import PERFILES, JugadorSimulado
from ia_models.simulador import jugar_partida


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--partidas", type=int, default=2000)
    parser.add_argument("--semilla", type=int, default=42)
    args = parser.parse_args()

    banco = cargar_banco()
    geneticos = cargar_agentes()
    print(f"{'perfil':26}{'agente':12}{'puntaje':>8}{'abandonos':>11}{'modeladas':>11}{'estrella':>10}")
    for perfil in PERFILES.values():
        for agente in (AgenteProgramado(), geneticos[perfil.id]):
            rng = random.Random(args.semilla)
            jugador = JugadorSimulado(perfil)
            partidas = [jugar_partida(banco, agente, rng, jugador=jugador) for _ in range(args.partidas)]
            rondas = [r for p in partidas for r in p.rondas]
            puntaje = mean(sum(perfil.puntaje(r) for r in p.rondas) for p in partidas)
            abandonos = mean(not r.resuelta for r in rondas)
            modeladas = mean(Ayuda.MODELAR in r.ayudas for r in rondas)
            estrella = mean(all(r.resuelta for r in p.rondas) and p.estrella() for p in partidas)
            print(f"{perfil.nombre:26}{agente.nombre:12}{puntaje:8.2f}{abandonos:11.1%}{modeladas:11.1%}{estrella:10.1%}")


if __name__ == "__main__":
    main()
