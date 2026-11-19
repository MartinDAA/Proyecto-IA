"""Generador de respuestas: traduce cada decisión del agente a pictogramas y texto para la voz."""

from dataclasses import dataclass

from ia_models.entorno import Ayuda, Partida
from ia_models.escenarios import Banco, Escenario


@dataclass
class Mensaje:
    pictogramas: list[str]
    texto: str


def _lista(nombres: list[str]) -> str:
    return ", ".join(nombres[:-1]) + " y " + nombres[-1] if len(nombres) > 1 else "".join(nombres)


def pregunta(banco: Banco, escenario: Escenario, categoria: str) -> Mensaje:
    cat = banco.categoria(categoria)
    return Mensaje(["que", cat.pictograma, "hay", "aqui"], f"¿Qué {cat.nombre} hay en {escenario.nombre}?")


def acierto(banco: Banco, elemento: str) -> Mensaje:
    return Mensaje(["bien", elemento], f"¡Muy bien! Es: {banco.pictogramas[elemento].nombre}.")


def error(banco: Banco, elegido: str) -> str:
    return f"{banco.pictogramas[elegido].nombre.capitalize()} no va aquí."


def ayuda(banco: Banco, partida: Partida, accion: Ayuda) -> Mensaje:
    ronda = partida.ronda
    correcto = banco.pictogramas[ronda.correcto]
    match accion:
        case Ayuda.RESALTAR:
            return Mensaje(["mira"], "Mira la parte del paisaje que brilla.")
        case Ayuda.PISTA:
            return Mensaje(list(correcto.pista), f"Una pista: {correcto.texto_pista}")
        case Ayuda.MODELAR:
            return Mensaje(["mira", correcto.id], f"Mira, es: {correcto.nombre}. Tócalo.")


def resumen(banco: Banco, partida: Partida) -> tuple[Mensaje, list[Mensaje]]:
    """Frase final con los aciertos y los elementos que el jugador eligió y no pertenecen."""
    e = partida.escenario
    elementos = [r.correcto for r in partida.rondas]
    nombres = [banco.pictogramas[x].nombre for x in elementos]
    frase = Mensaje([e.id, "tiene", *elementos], f"¡Terminaste! En {e.nombre} hay: {_lista(nombres)}.")
    vistos: list[str] = []
    for r in partida.rondas:
        vistos += [d for d in r.distractores_elegidos if d not in vistos]
    no_pertenecen = [
        Mensaje([d, "no", "aqui"], f"{banco.pictogramas[d].nombre.capitalize()} no va en {e.nombre}.")
        for d in vistos
    ]
    return frase, no_pertenecen
