#!/usr/bin/env python3
"""Crea la ficha de un proyecto nuevo a partir de una plantilla y lo añade a fichas/orden.txt.

Uso (desde la carpeta del portfolio):
    python3 tools/nuevo-proyecto.py mi-proyecto confidencial
    python3 tools/nuevo-proyecto.py mi-proyecto abierto

Después: edita fichas/mi-proyecto.txt y ejecuta  python3 tools/construir.py
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHAS = os.path.join(RAIZ, "fichas")


def main():
    a = sys.argv[1:]
    if len(a) != 2 or a[1] not in ("confidencial", "abierto"):
        print(__doc__)
        sys.exit(1)
    slug, tipo = a
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", slug):
        print("El nombre solo puede llevar minúsculas, números y guiones (ej. banca-app).")
        sys.exit(1)
    destino = os.path.join(FICHAS, slug + ".txt")
    if os.path.exists(destino):
        print(f"Ya existe fichas/{slug}.txt; no lo sobrescribo.")
        sys.exit(1)
    with open(os.path.join(FICHAS, f"_plantilla-{tipo}.txt"), encoding="utf-8") as f:
        texto = f.read()
    texto = re.sub(r"^archivo: mi-proyecto\b", f"archivo: {slug}", texto, flags=re.M)
    texto = texto.replace("mi-proyecto", slug)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(texto)
    orden = os.path.join(FICHAS, "orden.txt")
    with open(orden, encoding="utf-8") as f:
        lineas = f.read().split("\n")
    # se añade el primero de la lista (arriba del todo = el más reciente)
    i = next((n for n, l in enumerate(lineas) if l.strip() and not l.lstrip().startswith("#")), len(lineas))
    lineas.insert(i, slug)
    with open(orden, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))
    print(f"Creado fichas/{slug}.txt ({tipo}) y añadido el primero en fichas/orden.txt.")
    print("Siguiente: edita la ficha, sube la portada a assets/img/" + slug + ".jpg y ejecuta  python3 tools/construir.py")


if __name__ == "__main__":
    main()
