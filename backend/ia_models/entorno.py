"""Entorno del juego: estado de la partida y reglas de transición."""

import random
from dataclasses import dataclass, field
from enum import IntEnum

from ia_models.escenarios import Banco, Escenario

CATEGORIAS = ("animal", "construccion", "transporte", "objeto")


class Ayuda(IntEnum):
    """Ayudas del agente, de la más leve a la más directa."""

    RESALTAR = 1
    PISTA = 2
    MODELAR = 3


@dataclass
class Ronda:
    categoria: str
    correcto: str
    opciones: list[str]
    errores: int = 0
    ayudas: list[Ayuda] = field(default_factory=list)
    elegidos: list[str] = field(default_factory=list)
    resuelta: bool = False

    @property
    def distractores_elegidos(self) -> list[str]:
        return [p for p in self.elegidos if p != self.correcto]


@dataclass
class Partida:
    banco: Banco
    escenario: Escenario
    rng: random.Random = field(default_factory=random.Random)
    rondas: list[Ronda] = field(default_factory=list)

    @property
    def ronda(self) -> Ronda:
        return self.rondas[-1]

    @property
    def terminada(self) -> bool:
        return len(self.rondas) == len(CATEGORIAS) and self.ronda.resuelta

    def iniciar_ronda(self) -> Ronda:
        categoria = CATEGORIAS[len(self.rondas)]
        correcto = self.escenario.objetivo[categoria]
        opciones = [correcto, *self.banco.distractores(self.escenario, categoria, self.rng)]
        self.rng.shuffle(opciones)
        self.rondas.append(Ronda(categoria, correcto, opciones))
        return self.ronda

    def responder(self, pictograma: str) -> bool:
        """Transición ante la selección del jugador. Devuelve si fue correcta."""
        r = self.ronda
        if pictograma not in r.opciones:
            raise ValueError(f"'{pictograma}' no es una opción de la ronda")
        r.elegidos.append(pictograma)
        if pictograma == r.correcto:
            r.resuelta = True
            return True
        r.errores += 1
        r.opciones.remove(pictograma)
        return False

    def aplicar_ayuda(self, ayuda: Ayuda) -> None:
        self.ronda.ayudas.append(ayuda)

    def estrella(self) -> bool:
        """Victoria: al menos 3 de 4 rondas resueltas sin que se le muestre la respuesta."""
        return sum(1 for r in self.rondas if Ayuda.MODELAR not in r.ayudas) >= 3

    def aciertos_primer_intento(self) -> int:
        return sum(1 for r in self.rondas if r.errores == 0)
