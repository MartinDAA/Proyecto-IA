from fastapi import APIRouter, HTTPException, status

from app.dependencies import CurrentUser, PartidaServiceDep
from app.models.partida import EscenarioOut, IniciarRequest, ResponderRequest, TurnoOut
from app.services.partida_service import PartidaNoEncontrada

router = APIRouter(prefix="/api", tags=["partida"])


@router.get("/escenarios")
def escenarios(_: CurrentUser, service: PartidaServiceDep) -> list[EscenarioOut]:
    return service.escenarios()


@router.post("/partida/iniciar")
def iniciar(request: IniciarRequest, user: CurrentUser, service: PartidaServiceDep) -> TurnoOut:
    try:
        return service.iniciar(request.escenario_id, user.username)
    except PartidaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/partida/responder")
def responder(request: ResponderRequest, user: CurrentUser, service: PartidaServiceDep) -> TurnoOut:
    try:
        return service.responder(request.partida_id, request.pictograma, user.username)
    except PartidaNoEncontrada as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
