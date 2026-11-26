"""Guarda en el frontend una copia de cada pictograma de ARASAAC que usa el juego.

Así el juego funciona sin internet y ninguna opción aparece en blanco mientras carga.
Reúne los identificadores de datos/escenarios.json y de frontend/src/lib/guia.ts, y escribe
frontend/static/pictogramas/<id>.webp: 300 px (el más grande se ve a unos 180 px), salvo los
paisajes, a 700 px porque ocupan toda la escena.
Volver a ejecutarlo al agregar pictogramas.
Licencia: CC BY-NC-SA, citando a ARASAAC (el pie de la pantalla principal ya lo hace).

Uso (desde backend/):
    uv run --with pillow python -m ia_models.herramientas.descargar_pictogramas
"""

import io
import re
import urllib.request

from ia_models.escenarios import cargar_banco
from ia_models.herramientas.generar_audios import FRONTEND

SALIDA = FRONTEND / "static" / "pictogramas"
GUIA = FRONTEND / "src" / "lib" / "guia.ts"
# Pictogramas de la guía: p('id', 'nombre', 'emoji', 1234).
LADO = 300
LADO_PAISAJE = 700
PATRON_GUIA = re.compile(r"\bp\('[^']*', '[^']*', '[^']*', (\d+)\)")


def identificadores() -> set[int]:
    del_banco = {p.arasaac for p in cargar_banco().pictogramas.values() if p.arasaac}
    return del_banco | {int(i) for i in PATRON_GUIA.findall(GUIA.read_text(encoding="utf-8"))}


def main() -> None:
    from PIL import Image  # solo se necesita para descargar

    SALIDA.mkdir(parents=True, exist_ok=True)
    ids = sorted(identificadores())
    grandes = paisajes()
    for i in ids:
        destino = SALIDA / f"{i}.webp"
        lado = LADO_PAISAJE if i in grandes else LADO
        if destino.exists() and Image.open(destino).width == lado:
            continue
        url = f"https://static.arasaac.org/pictograms/{i}/{i}_{2500 if i in grandes else 500}.png"
        with urllib.request.urlopen(url, timeout=30) as respuesta:
            imagen = Image.open(io.BytesIO(respuesta.read())).convert("RGBA")
        imagen.resize((lado, lado), Image.Resampling.LANCZOS).save(destino, "WEBP", quality=85)
        print(f"{i} ✓")
    print(f"{len(ids)} pictogramas en {SALIDA}")


def paisajes() -> set[int]:
    banco = cargar_banco()
    return {banco.pictogramas[e].arasaac for e in banco.escenarios}


if __name__ == "__main__":
    main()
