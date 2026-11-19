"""Experimento A: simulación en consola del agente guiando una partida.

A partir de un estado inicial (un escenario), el agente pregunta con pictogramas, evalúa cada
respuesta de un jugador simulado y da la siguiente ayuda de su guion tras cada error.

Uso (desde backend/):
    uv run python -m ia_models.experimento_a
    uv run python -m ia_models.experimento_a --escenario playa --semilla 7
"""

import argparse
import random

from ia_models import generador
from ia_models.agentes import AgenteProgramado
from ia_models.entorno import Ayuda, Partida
from ia_models.escenarios import cargar_banco
from ia_models.simulador import jugar_partida


def pictos(banco, ids: list[str]) -> str:
    return " + ".join(f"[{banco.pictogramas[i].nombre.upper()}]" for i in ids)


def main() -> None:
    banco = cargar_banco()
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--escenario", choices=list(banco.escenarios), default="granja")
    parser.add_argument("--semilla", type=int, default=42)
    args = parser.parse_args()

    print(f"== Partida guiada: escenario '{args.escenario}' ==")

    def observar(evento: str, partida: Partida, datos: dict) -> None:
        ronda = partida.ronda
        if evento == "ronda":
            p = generador.pregunta(banco, partida.escenario, ronda.categoria)
            print(f"\nRonda {len(partida.rondas)} ({ronda.categoria})")
            print(f"  Agente  : {pictos(banco, p.pictogramas)}  «{p.texto}»")
            print(f"  Opciones: {pictos(banco, ronda.opciones)}")
        elif evento == "respuesta":
            nombre = banco.pictogramas[datos["elegido"]].nombre.upper()
            if datos["correcto"]:
                m = generador.acierto(banco, datos["elegido"])
                print(f"  Jugador : [{nombre}] ✔  {pictos(banco, m.pictogramas)}  «{m.texto}»")
            else:
                print(f"  Jugador : [{nombre}] ✘  «{generador.error(banco, datos['elegido'])}»")
        elif evento == "ayuda":
            a: Ayuda = datos["ayuda"]
            m = generador.ayuda(banco, partida, a)
            print(f"  Ayuda {int(a)} ({a.name.lower()})")
            print(f"  Agente  : {pictos(banco, m.pictogramas)}  «{m.texto}»")
            print(f"  Opciones: {pictos(banco, ronda.opciones)}")
        elif evento == "fin":
            frase, no_van = generador.resumen(banco, partida)
            print(f"\nResumen : {pictos(banco, frase.pictogramas)}  «{frase.texto}»")
            for m in no_van:
                print(f"          {pictos(banco, m.pictogramas)}  «{m.texto}»")
            estrella = "sí" if partida.estrella() else "no"
            print(f"Aciertos al primer intento: {partida.aciertos_primer_intento()}/4 · Estrella: {estrella}")

    jugar_partida(banco, AgenteProgramado(), random.Random(args.semilla), args.escenario, observar)


if __name__ == "__main__":
    main()
