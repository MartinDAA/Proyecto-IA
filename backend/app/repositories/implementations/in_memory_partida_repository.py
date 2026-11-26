import time
from threading import Lock

from app.repositories.partida_repository import PartidaRepository, SesionPartida

# Una partida dura minutos: pasado este tiempo se considera abandonada.
DURACION_MAXIMA = 2 * 60 * 60


class InMemoryPartidaRepository(PartidaRepository):
    """Guarda las partidas en memoria: se pierden al reiniciar."""

    def __init__(self) -> None:
        self._partidas: dict[str, SesionPartida] = {}
        self._lock = Lock()

    def get(self, id: str) -> SesionPartida | None:
        return self._partidas.get(id)

    def save(self, sesion: SesionPartida) -> None:
        """Guarda la partida y descarta las terminadas y las abandonadas."""
        limite = time.monotonic() - DURACION_MAXIMA
        with self._lock:
            self._partidas = {
                id: s for id, s in self._partidas.items() if not s.partida.terminada and s.creada > limite
            }
            self._partidas[sesion.id] = sesion
