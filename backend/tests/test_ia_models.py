import random

from ia_models.agentes import AgenteProgramado
from ia_models.entorno import Ayuda, Partida
from ia_models.escenarios import cargar_banco
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
