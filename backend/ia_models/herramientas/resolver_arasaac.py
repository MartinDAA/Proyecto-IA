"""Completa el identificador de ARASAAC de cada pictograma del banco de escenarios.

Busca en la API pública de ARASAAC (https://arasaac.org) el término `buscar` (o el nombre) de cada
pictograma que todavía no tiene `arasaac` y guarda el primer resultado. Conviene revisar
visualmente los pictogramas obtenidos y corregir a mano los que no correspondan.

Uso (desde backend/):  uv run python -m ia_models.herramientas.resolver_arasaac
"""

import json
import urllib.parse
import urllib.request

from ia_models.escenarios import ruta_escenarios

API = "https://api.arasaac.org/v1/pictograms/es"


def buscar(termino: str) -> int | None:
    for modo in ("bestsearch", "search"):
        url = f"{API}/{modo}/{urllib.parse.quote(termino)}"
        try:
            with urllib.request.urlopen(url, timeout=15) as response:
                resultados = json.load(response)
        except Exception:
            continue
        if resultados:
            return resultados[0]["_id"]
    return None


def guardar(datos: dict, ruta) -> None:
    # Un pictograma por línea para que el archivo siga siendo fácil de editar a mano.
    pictos = ",\n".join(
        f"    {json.dumps(k, ensure_ascii=False)}: {json.dumps(v, ensure_ascii=False)}"
        for k, v in datos["pictogramas"].items()
    )
    resto = {k: v for k, v in datos.items() if k != "pictogramas"}
    cuerpo = json.dumps(resto, ensure_ascii=False, indent=2)
    texto = cuerpo.replace('{\n  "categorias"', '{\n  "pictogramas": {\n' + pictos + '\n  },\n  "categorias"', 1)
    ruta.write_text(texto + "\n", encoding="utf-8")


def main() -> None:
    ruta = ruta_escenarios()
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    for clave, picto in datos["pictogramas"].items():
        if picto.get("arasaac"):
            continue
        picto["arasaac"] = buscar(picto.get("buscar", picto["nombre"]).strip("¿?¡!"))
        print(f"{clave:20} → {picto['arasaac']}")
    guardar(datos, ruta)


if __name__ == "__main__":
    main()
