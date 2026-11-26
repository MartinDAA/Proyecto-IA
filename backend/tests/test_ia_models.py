import random
from itertools import product
from statistics import mean

import pytest

from app.repositories.implementations.in_memory_partida_repository import DURACION_MAXIMA, InMemoryPartidaRepository
from app.repositories.partida_repository import SesionPartida
from ia_models import csp
from ia_models.agentes import GUION, AgenteProgramado, cargar_agentes
from ia_models.entorno import CATEGORIAS, Ayuda, Partida
from ia_models.escenarios import SinDistractores, cargar_banco
from ia_models.herramientas.entrenar_politicas import evolucionar
from ia_models.jugador import PERFILES, JugadorSimulado, valor, valor_ronda
from ia_models.simulador import jugar_partida

banco = cargar_banco()


def test_banco_completo():
    assert len(banco.escenarios) == 10
    for e in banco.escenarios.values():
        for categoria, elemento in e.objetivo.items():
            assert banco.pictogramas[elemento].categoria == categoria


def test_distractores_no_pertenecen_al_escenario():
    rng = random.Random(0)
    for e in banco.escenarios.values():
        for categoria in e.objetivo:
            d = banco.distractores(e, categoria, rng)
            assert len(set(d)) == 3
            assert e.objetivo[categoria] not in d
            assert not set(d) & e.compatibles


def test_error_retira_la_opcion():
    partida = Partida(banco, banco.escenarios["granja"], rng=random.Random(0))
    ronda = partida.iniciar_ronda()
    incorrecto = next(o for o in ronda.opciones if o != "vaca")
    assert partida.responder(incorrecto) is False
    assert incorrecto not in ronda.opciones and ronda.errores == 1
    assert partida.responder("vaca") is True


def test_guion_de_ayudas():
    agente = AgenteProgramado()
    partida = Partida(banco, banco.escenarios["granja"], rng=random.Random(0))
    ronda = partida.iniciar_ronda()
    for esperada in (Ayuda.RESALTAR, Ayuda.PISTA, Ayuda.MODELAR):
        ayuda = agente.elegir_ayuda(ronda)
        assert ayuda == esperada
        partida.aplicar_ayuda(ayuda)


def test_partidas_simuladas_terminan_sin_repetir_ayudas():
    rng = random.Random(1)
    for _ in range(200):
        partida = jugar_partida(banco, AgenteProgramado(), rng)
        assert partida.terminada
        assert all(len(r.ayudas) == len(set(r.ayudas)) for r in partida.rondas)


def test_csp_retrocede_y_detecta_que_no_hay_solucion():
    distintos = str.__ne__
    # Con "a" primero, la primera variable debe retroceder a "b".
    assert csp.resolver([["a", "b"], ["a", "c"], ["a", "c"]], distintos) == ["b", "a", "c"]
    assert csp.resolver([["a", "b"]] * 3, distintos) is None
    assert csp.ac3([["a", "b"], ["a"]], distintos) == [["b"], ["a"]]


def test_distractores_de_ambientes_distintos_y_variados():
    rng = random.Random(0)
    for e in banco.escenarios.values():
        for categoria in CATEGORIAS:
            rondas = [banco.distractores(e, categoria, rng) for _ in range(30)]
            assert all(len({banco.pictogramas[d].ambiente for d in r}) == 3 for r in rondas)
            assert len({frozenset(r) for r in rondas}) > 1


def test_distractores_relaja_ambientes_y_avisa_si_no_alcanzan():
    rng = random.Random(0)
    granja = banco.escenarios["granja"]
    agua = {p.id for p in banco.pictogramas.values() if p.ambiente == "agua"}
    # Solo quedan tres elementos del agua: se relaja la regla de ambientes.
    evitar = frozenset(banco.elementos_de("transporte")) - {"velero", "canoa", "barco_carga"}
    assert set(banco.distractores(granja, "transporte", rng, evitar=evitar)) <= agua
    with pytest.raises(SinDistractores):
        banco.distractores(granja, "transporte", rng, evitar=evitar | {"canoa"})


@pytest.mark.parametrize("perfil", PERFILES.values(), ids=lambda p: p.id)
def test_politicas_guardadas_son_optimas(perfil):
    """Si falla tras cambiar jugador.py: volver a ejecutar entrenar_politicas."""
    # La aptitud se separa por categoría, así que el óptimo se puede comprobar probándolo todo.
    optimo = sum(max(valor_ronda(perfil, c, f) for f in product(Ayuda, repeat=3)) for c in CATEGORIAS)
    assert valor(perfil, cargar_agentes()[perfil.id].politica) == pytest.approx(optimo)
    assert valor(perfil, evolucionar(perfil, random.Random(7))[0]) == pytest.approx(optimo)
    assert optimo > valor(perfil, {c: GUION for c in CATEGORIAS})


def test_valor_coincide_con_partidas_simuladas():
    perfil = PERFILES["estandar"]
    agente = cargar_agentes()["estandar"]
    rng = random.Random(0)
    jugador = JugadorSimulado(perfil)
    partidas = [jugar_partida(banco, agente, rng, "granja", jugador=jugador) for _ in range(5000)]
    puntaje = mean(sum(perfil.puntaje(r) for r in p.rondas) for p in partidas)
    assert puntaje == pytest.approx(valor(perfil, agente.politica), abs=0.7)


def test_repositorio_descarta_partidas_terminadas_y_viejas():
    repo = InMemoryPartidaRepository()
    for id in ("terminada", "vieja", "actual"):
        repo.save(SesionPartida(id, Partida(banco, banco.escenarios["granja"], rng=random.Random(0)), "estandar"))
    repo.get("terminada").partida = jugar_partida(banco, AgenteProgramado(), random.Random(0))
    repo.get("vieja").creada -= DURACION_MAXIMA
    for p in ("actual", "vieja"):
        repo.get(p).partida.iniciar_ronda()
    repo.save(repo.get("actual"))
    assert repo.get("actual") and repo.get("terminada") is None and repo.get("vieja") is None
