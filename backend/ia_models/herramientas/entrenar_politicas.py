"""Algoritmo genético: calcula, fuera del servidor, la política de ayudas de cada perfil.

Cromosoma: 12 genes (ayuda tras el error 1, 2 y 3 en cada una de las 4 categorías).
Aptitud: puntaje esperado de la partida según el jugador simulado (ia_models/jugador.py).
Escribe datos/politicas.json. Volver a ejecutarlo si cambia jugador.py.

Uso (desde backend/):  uv run python -m ia_models.herramientas.entrenar_politicas
"""

import argparse
import json
import random
from math import isclose

from ia_models.agentes import GUION, POLITICAS
from ia_models.entorno import CATEGORIAS, Ayuda
from ia_models.jugador import PERFILES, Perfil, Politica, valor, valor_ronda

POBLACION = 24
TORNEO = 3
CRUCE = 0.9
MUTACION = 0.06
ELITE = 2
GENERACIONES = 60
ERRORES = 3
GENES = ERRORES * len(CATEGORIAS)

Cromosoma = tuple[Ayuda, ...]


def decodificar(cromosoma: Cromosoma) -> Politica:
    return {c: cromosoma[i * ERRORES : (i + 1) * ERRORES] for i, c in enumerate(CATEGORIAS)}


def normalizar(perfil: Perfil, politica: Politica) -> Politica:
    """Fija los genes que no cambian la aptitud, que si no quedarían al azar.

    Tras modelar se sigue modelando; en un empate se prefiere una ayuda que no se haya dado.
    """

    def ajustar(categoria: str, fila: tuple[Ayuda, ...]) -> tuple[Ayuda, ...]:
        optimo = valor_ronda(perfil, categoria, fila)
        for i in range(ERRORES):
            opciones = [Ayuda.MODELAR] if Ayuda.MODELAR in fila[:i] else [a for a in Ayuda if a not in fila[:i]]
            for a in opciones:
                alterna = (*fila[:i], a, *fila[i + 1 :])
                if isclose(valor_ronda(perfil, categoria, alterna), optimo):
                    fila = alterna
                    break
        return fila

    return {c: ajustar(c, fila) for c, fila in politica.items()}


def evolucionar(perfil: Perfil, rng: random.Random) -> tuple[Politica, list[float]]:
    """Devuelve la mejor política y la mejor aptitud de cada generación."""

    def aptitud(c: Cromosoma) -> float:
        return valor(perfil, decodificar(c))

    def torneo() -> Cromosoma:
        return max(rng.sample(poblacion, TORNEO), key=aptitud)

    def mutar(gen: Ayuda) -> Ayuda:
        return rng.choice([a for a in Ayuda if a != gen]) if rng.random() < MUTACION else gen

    poblacion = [tuple(rng.choices(list(Ayuda), k=GENES)) for _ in range(POBLACION)]
    poblacion.sort(key=aptitud, reverse=True)
    historial = [aptitud(poblacion[0])]
    for _ in range(GENERACIONES):
        hijos = poblacion[:ELITE]
        while len(hijos) < POBLACION:
            a, b = torneo(), torneo()
            corte = rng.randint(1, GENES - 1) if rng.random() < CRUCE else GENES
            hijos.append(tuple(mutar(g) for g in a[:corte] + b[corte:]))
        poblacion = sorted(hijos, key=aptitud, reverse=True)
        historial.append(aptitud(poblacion[0]))
    return normalizar(perfil, decodificar(poblacion[0])), historial


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--semilla", type=int, default=42)
    args = parser.parse_args()

    salida = {}
    for perfil in PERFILES.values():
        politica, historial = evolucionar(perfil, random.Random(args.semilla))
        base = valor(perfil, {c: GUION for c in CATEGORIAS})
        print(f"\n{perfil.nombre}: guion {base:.2f} → AG {historial[-1]:.2f}")
        print("  mejor por generación (cada 10): " + "  ".join(f"{h:.2f}" for h in historial[::10]))
        for c, fila in politica.items():
            print(f"  {c:13} {' → '.join(a.name.lower() for a in fila)}")
        salida[perfil.id] = {
            "aptitud": round(historial[-1], 2),
            "politica": {c: [a.name.lower() for a in fila] for c, fila in politica.items()},
        }
    POLITICAS.write_text(json.dumps(salida, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n→ {POLITICAS}")


if __name__ == "__main__":
    main()
