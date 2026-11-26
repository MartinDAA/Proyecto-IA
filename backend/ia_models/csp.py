"""CSP binario: consistencia de arcos (AC-3) y backtracking."""

from collections import deque
from collections.abc import Callable

Restriccion = Callable[[str, str], bool]


def ac3(dominios: list[list[str]], compatibles: Restriccion) -> list[list[str]]:
    """Borra de cada dominio los valores que no tienen soporte en otra variable."""
    dominios = [list(d) for d in dominios]
    n = len(dominios)
    cola = deque((i, j) for i in range(n) for j in range(n) if i != j)
    while cola:
        i, j = cola.popleft()
        con_soporte = [x for x in dominios[i] if any(compatibles(x, y) for y in dominios[j])]
        if len(con_soporte) < len(dominios[i]):
            dominios[i] = con_soporte
            cola.extend((k, i) for k in range(n) if k not in (i, j))
    return dominios


def resolver(dominios: list[list[str]], compatibles: Restriccion) -> list[str] | None:
    """Asigna un valor a cada variable respetando la restricción en todos los pares, o None."""
    dominios = ac3(dominios, compatibles)

    def backtracking(asignados: list[str]) -> list[str] | None:
        if len(asignados) == len(dominios):
            return asignados
        for valor in dominios[len(asignados)]:
            if all(compatibles(a, valor) for a in asignados):
                if solucion := backtracking([*asignados, valor]):
                    return solucion
        return None

    return backtracking([])
