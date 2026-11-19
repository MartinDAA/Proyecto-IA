"""Agente con respuestas programadas: tras cada error da la siguiente ayuda del guion."""

from ia_models.entorno import Ayuda, Ronda

# Orden fijo de ayudas: de la más leve a la que muestra la respuesta.
GUION = (Ayuda.RESALTAR, Ayuda.PISTA, Ayuda.MODELAR)


class AgenteProgramado:
    nombre = "programado"

    def elegir_ayuda(self, ronda: Ronda) -> Ayuda:
        # Con 4 opciones hay como máximo 3 errores, así que el guion siempre alcanza.
        return GUION[min(len(ronda.ayudas), len(GUION) - 1)]
