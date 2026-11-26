import random
import uuid
from collections.abc import Mapping

from app.models.partida import (
    AyudaOut,
    CategoriaOut,
    EscenarioOut,
    MensajeOut,
    PerfilOut,
    PictogramaOut,
    ResumenOut,
    TurnoOut,
)
from app.repositories.partida_repository import PartidaRepository, SesionPartida
from ia_models import generador
from ia_models.agentes import Agente
from ia_models.entorno import CATEGORIAS, Ayuda, Partida
from ia_models.escenarios import Banco, Escenario
from ia_models.jugador import PERFILES


class PartidaNoEncontrada(Exception):
    pass


class PartidaService:
    """Orquesta la partida: Captura → Motor de Decisión (agente) → Generador de Respuestas."""

    def __init__(self, partidas: PartidaRepository, agentes: Mapping[str, Agente], banco: Banco) -> None:
        self.partidas = partidas
        # Un agente por perfil.
        self.agentes = agentes
        self.banco = banco

    # ------------------------------------------------------------------ consultas
    def escenarios(self) -> list[EscenarioOut]:
        return [self._escenario(e) for e in self.banco.escenarios.values()]

    def perfiles(self) -> list[PerfilOut]:
        return [PerfilOut(id=p.id, nombre=p.nombre, descripcion=p.descripcion) for p in PERFILES.values()]

    # ------------------------------------------------------------------ acciones
    def iniciar(self, escenario_id: str, perfil: str, evitar: frozenset[str]) -> TurnoOut:
        escenario = self.banco.escenarios.get(escenario_id)
        if escenario is None:
            raise PartidaNoEncontrada(f"No existe el escenario '{escenario_id}'")
        if perfil not in self.agentes:
            raise PartidaNoEncontrada(f"No existe el perfil '{perfil}'")
        if evitar & set(escenario.objetivo.values()):
            raise ValueError(f"En {escenario.nombre} aparece un elemento a evitar.")
        partida = Partida(self.banco, escenario, rng=random.Random(), evitar=evitar)
        # Se comprueba antes de empezar que todas las rondas tienen distractores.
        for categoria in CATEGORIAS:
            self.banco.distractores(escenario, categoria, partida.rng, evitar=evitar)
        partida.iniciar_ronda()
        sesion = SesionPartida(str(uuid.uuid4()), partida, perfil)
        self.partidas.save(sesion)
        return self._turno(sesion)

    def responder(self, partida_id: str, pictograma: str) -> TurnoOut:
        sesion = self.partidas.get(partida_id)
        if sesion is None:
            raise PartidaNoEncontrada("No existe la partida")
        partida = sesion.partida
        if partida.terminada:
            raise ValueError("La partida ya terminó")
        ronda = partida.ronda

        if partida.responder(pictograma):
            retro = generador.acierto(self.banco, pictograma)
            if not partida.terminada:
                partida.iniciar_ronda()
            return self._turno(sesion, retro=retro, elegido=pictograma, correcto=True)

        accion = self.agentes[sesion.perfil].elegir_ayuda(ronda)
        partida.aplicar_ayuda(accion)
        retro = generador.Mensaje([pictograma, "no", "aqui"], generador.error(self.banco, pictograma))
        return self._turno(sesion, retro=retro, elegido=pictograma, correcto=False, ayuda=accion)

    # ------------------------------------------------------------------ respuestas
    def _picto(self, id: str) -> PictogramaOut:
        p = self.banco.pictogramas[id]
        # Copia local, servida por el frontend (ia_models/herramientas/descargar_pictogramas.py).
        imagen = f"/pictogramas/{p.arasaac}.webp" if p.arasaac else None
        return PictogramaOut(id=p.id, nombre=p.nombre, emoji=p.emoji, imagen=imagen)

    def _mensaje(self, m: generador.Mensaje) -> MensajeOut:
        return MensajeOut(pictogramas=[self._picto(p) for p in m.pictogramas], texto=m.texto)

    def _escenario(self, e: Escenario) -> EscenarioOut:
        return EscenarioOut(
            id=e.id,
            nombre=e.nombre,
            cielo=e.cielo,
            pictograma=self._picto(e.id),
            elementos=[self._picto(e.objetivo[c]) for c in CATEGORIAS],
        )

    def _turno(
        self,
        sesion: SesionPartida,
        retro: generador.Mensaje | None = None,
        elegido: str | None = None,
        correcto: bool | None = None,
        ayuda: Ayuda | None = None,
    ) -> TurnoOut:
        partida = sesion.partida
        ronda = partida.ronda
        categoria = self.banco.categoria(ronda.categoria)
        resumen = None
        if partida.terminada:
            frase, no_van = generador.resumen(self.banco, partida)
            mensaje = frase
            resumen = ResumenOut(
                frase=self._mensaje(frase),
                no_pertenecen=[self._mensaje(m) for m in no_van],
                aciertos_primer_intento=partida.aciertos_primer_intento(),
                estrella=partida.estrella(),
                terminar=self._picto("terminar"),
            )
        elif ayuda is not None:
            mensaje = generador.ayuda(self.banco, partida, ayuda)
        else:
            mensaje = generador.pregunta(self.banco, partida.escenario, ronda.categoria)

        return TurnoOut(
            partida_id=sesion.id,
            escenario=self._escenario(partida.escenario),
            ronda=len(partida.rondas),
            total_rondas=len(CATEGORIAS),
            categoria=CategoriaOut(id=categoria.id, nombre=categoria.nombre, pictograma=self._picto(categoria.pictograma)),
            opciones=[self._picto(o) for o in ronda.opciones],
            mensaje=self._mensaje(mensaje),
            retro=self._mensaje(retro) if retro else None,
            elegido=elegido,
            correcto=correcto,
            ayuda=AyudaOut(accion=ayuda.name.lower(), nivel=int(ayuda)) if ayuda is not None else None,
            resaltar=ronda.correcto if Ayuda.RESALTAR in ronda.ayudas and not ronda.resuelta else None,
            destacar=ronda.correcto if Ayuda.MODELAR in ronda.ayudas and not ronda.resuelta else None,
            terminada=partida.terminada,
            resumen=resumen,
        )
