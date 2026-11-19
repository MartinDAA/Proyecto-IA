from abc import ABC, abstractmethod
from dataclasses import dataclass

from ia_models.entorno import Partida


@dataclass
class SesionPartida:
    id: str
    usuario: str
    partida: Partida


class PartidaRepository(ABC):
    @abstractmethod
    def get(self, id: str) -> SesionPartida | None: ...

    @abstractmethod
    def save(self, sesion: SesionPartida) -> None: ...
