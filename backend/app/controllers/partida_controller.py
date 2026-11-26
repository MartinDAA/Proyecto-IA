from fastapi import APIRouter, HTTPException, status

from app.dependencies import PartidaServiceDep
from app.models.partida import EscenarioOut, IniciarRequest, PerfilOut, ResponderRequest, TurnoOut
from app.services.partida_service import PartidaNoEncontrada

router = APIRouter(prefix="/api", tags=["partida"])


@router.get("/escenarios")
def escenarios(service: PartidaServiceDep) -> list[EscenarioOut]:
    return service.escenarios()


@router.get("/perfiles")
def perfiles(service: PartidaServiceDep) -> list[PerfilOut]:
    return service.perfiles()


@router.post("/partida/iniciar")
def iniciar(request: IniciarRequest, service: PartidaServiceDep) -> TurnoOut:
    try:
        return service.iniciar(request.escenario_id, request.perfil, frozenset(request.evitar))
    except PartidaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e


@router.post("/partida/responder")
def responder(request: ResponderRequest, service: PartidaServiceDep) -> TurnoOut:
    try:
        return service.responder(request.partida_id, request.pictograma)
    except PartidaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
