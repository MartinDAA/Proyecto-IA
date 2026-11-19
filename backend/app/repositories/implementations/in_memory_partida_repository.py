from app.repositories.partida_repository import PartidaRepository, SesionPartida


class InMemoryPartidaRepository(PartidaRepository):
    """Guarda las partidas en memoria: se pierden al reiniciar."""

    def __init__(self) -> None:
        self._partidas: dict[str, SesionPartida] = {}

    def get(self, id: str) -> SesionPartida | None:
        return self._partidas.get(id)

    def save(self, sesion: SesionPartida) -> None:
        self._partidas[sesion.id] = sesion
