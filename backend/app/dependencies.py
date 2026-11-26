from typing import Annotated

from fastapi import Depends

from app.repositories.implementations.in_memory_partida_repository import InMemoryPartidaRepository
from app.repositories.partida_repository import PartidaRepository
from app.services.partida_service import PartidaService
from ia_models.agentes import cargar_agentes
from ia_models.escenarios import cargar_banco

# Instancia única: el repositorio en memoria debe compartirse entre peticiones.
_partida_repository = InMemoryPartidaRepository()
_agentes = cargar_agentes()


def get_partida_repository() -> PartidaRepository:
    return _partida_repository


def get_partida_service(
    partidas: Annotated[PartidaRepository, Depends(get_partida_repository)],
) -> PartidaService:
    return PartidaService(partidas, _agentes, cargar_banco())


PartidaServiceDep = Annotated[PartidaService, Depends(get_partida_service)]
