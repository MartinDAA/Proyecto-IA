from pydantic import BaseModel, Field


class PictogramaOut(BaseModel):
    id: str
    nombre: str
    emoji: str
    # URL del pictograma de ARASAAC; si no carga, el frontend muestra el emoji.
    imagen: str | None


class EscenarioOut(BaseModel):
    id: str
    nombre: str
    cielo: str
    pictograma: PictogramaOut
    # Elementos que aparecen en el paisaje (uno por categoría).
    elementos: list[PictogramaOut]


class CategoriaOut(BaseModel):
    id: str
    nombre: str
    pictograma: PictogramaOut


class MensajeOut(BaseModel):
    pictogramas: list[PictogramaOut]
    texto: str


class AyudaOut(BaseModel):
    accion: str
    nivel: int


class ResumenOut(BaseModel):
    frase: MensajeOut
    no_pertenecen: list[MensajeOut]
    aciertos_primer_intento: int
    estrella: bool
    # Pictograma del botón para volver a la pantalla principal.
    terminar: PictogramaOut


class TurnoOut(BaseModel):
    partida_id: str
    escenario: EscenarioOut
    ronda: int
    total_rondas: int
    categoria: CategoriaOut
    opciones: list[PictogramaOut]
    # Mensaje actual del agente (pregunta, pista o frase final).
    mensaje: MensajeOut
    # Retroalimentación a la última respuesta, que se muestra antes del mensaje.
    retro: MensajeOut | None = None
    elegido: str | None = None
    correcto: bool | None = None
    ayuda: AyudaOut | None = None
    # Elemento del paisaje que brilla (ayuda "resaltar").
    resaltar: str | None = None
    # Opción correcta que se destaca (ayuda "modelar").
    destacar: str | None = None
    terminada: bool = False
    resumen: ResumenOut | None = None


class IniciarRequest(BaseModel):
    escenario_id: str = Field(min_length=1)


class ResponderRequest(BaseModel):
    partida_id: str = Field(min_length=1)
    pictograma: str = Field(min_length=1)
