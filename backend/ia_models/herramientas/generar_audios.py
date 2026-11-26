"""Genera la voz pregrabada del juego con Piper (TTS offline), una sola vez.

Como todos los textos son fijos, se sintetizan de antemano: la voz es la misma en cualquier
dispositivo y no depende de internet. Reúne los textos del generador de respuestas (todas las
combinaciones del banco de escenarios) y los textos fijos del frontend, y escribe:
  frontend/static/audio/<hash>.mp3   un audio por texto
  frontend/src/lib/audio.json        índice texto → archivo (lo usa frontend/src/lib/voz.ts)
Los textos que no estén en el índice se leen con la voz del navegador.

Requisitos: ffmpeg y una voz de Piper descargada en backend/.voces, por ejemplo:
    cd .voces && uvx --from piper-tts python -m piper.download_voices es_MX-claude-high

Uso (desde backend/):
    uv run --with piper-tts python -m ia_models.herramientas.generar_audios
    uv run --with piper-tts python -m ia_models.herramientas.generar_audios --voz es_AR-daniela-high --forzar
"""

import argparse
import hashlib
import json
import re
import subprocess
import wave
from pathlib import Path

from ia_models import generador
from ia_models.entorno import CATEGORIAS, Ayuda, Partida, Ronda
from ia_models.escenarios import Banco, cargar_banco

BACKEND = Path(__file__).resolve().parents[2]
FRONTEND = BACKEND.parent / "frontend"
SALIDA = FRONTEND / "static" / "audio"
INDICE = FRONTEND / "src" / "lib" / "audio.json"
# Textos fijos del frontend: frases de Uku (m('...')) y llamadas hablar('...').
PATRON_FRONTEND = re.compile(r"""(?:\bm\(\s*|\bhablar\(\s*)'([^']+)'""")


def textos_backend(banco: Banco) -> set[str]:
    textos: set[str] = set()
    for e in banco.escenarios.values():
        # Debe coincidir con frontend/src/routes/+page.svelte (al tocar un paisaje).
        textos.add(f"Vamos a {e.nombre}.")
        for c in CATEGORIAS:
            textos.add(generador.pregunta(banco, e, c).texto)
        # Resumen: una partida completa en la que se eligieron todos los distractores posibles.
        partida = Partida(banco, e)
        for c in CATEGORIAS:
            correcto = e.objetivo[c]
            distractores = banco.candidatos(e, c)
            partida.rondas.append(Ronda(c, correcto, [], elegidos=[*distractores, correcto], resuelta=True))
        frase, no_van = generador.resumen(banco, partida)
        textos |= {frase.texto, *(m.texto for m in no_van)}

    una = next(iter(banco.escenarios.values()))
    for c in CATEGORIAS:
        for elemento in banco.elementos_de(c):
            textos |= {generador.acierto(banco, elemento).texto, generador.error(banco, elemento)}
            partida = Partida(banco, una, rondas=[Ronda(c, elemento, [])])
            textos |= {generador.ayuda(banco, partida, a).texto for a in Ayuda}
    return textos


def textos_frontend() -> set[str]:
    textos: set[str] = set()
    for archivo in (FRONTEND / "src").rglob("*"):
        if archivo.suffix in (".ts", ".svelte"):
            textos |= set(PATRON_FRONTEND.findall(archivo.read_text(encoding="utf-8")))
    return textos


def nombre(texto: str) -> str:
    return hashlib.sha1(texto.encode()).hexdigest()[:12] + ".mp3"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--voz", default="es_MX-claude-high", help="modelo de Piper en backend/.voces")
    parser.add_argument("--lento", type=float, default=1.15, help="mayor que 1 habla más pausado")
    parser.add_argument("--forzar", action="store_true", help="regenera también los audios existentes")
    args = parser.parse_args()

    from piper import PiperVoice, SynthesisConfig  # solo se necesita para generar

    voz = PiperVoice.load(BACKEND / ".voces" / f"{args.voz}.onnx")
    config = SynthesisConfig(length_scale=args.lento)
    SALIDA.mkdir(parents=True, exist_ok=True)

    textos = sorted(textos_backend(cargar_banco()) | textos_frontend())
    indice = {}
    for i, texto in enumerate(textos, 1):
        mp3 = SALIDA / nombre(texto)
        indice[texto] = mp3.name
        if mp3.exists() and not args.forzar:
            continue
        wav = mp3.with_suffix(".wav")
        with wave.open(str(wav), "wb") as w:
            voz.synthesize_wav(texto, w, syn_config=config)
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-ac", "1", "-b:a", "48k", str(mp3)],
            check=True,
        )
        wav.unlink()
        print(f"[{i}/{len(textos)}] {texto}")

    # Se borran los audios de textos que ya no existen.
    for viejo in SALIDA.glob("*.mp3"):
        if viejo.name not in indice.values():
            viejo.unlink()
    INDICE.write_text(json.dumps(indice, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(indice)} textos → {SALIDA}")


if __name__ == "__main__":
    main()
