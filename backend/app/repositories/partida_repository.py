import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ia_models.entorno import Partida


@dataclass
class SesionPartida:
    id: str
    partida: Partida
    perfil: str
    creada: float = field(default_factory=time.monotonic)


class PartidaRepository(ABC):
    @abstractmethod
    def get(self, id: str) -> SesionPartida | None: ...

    @abstractmethod
    def save(self, sesion: SesionPartida) -> None: ...
