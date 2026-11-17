#!/usr/bin/env python3
"""Comprueba que todas las claves de idioma (data-i18n...) tienen traducción al español.

Uso (desde la carpeta del portfolio):
    python3 tools/comprobar-idiomas.py

- FALTA:  la clave está en un HTML (o en tools/proteger.py) pero no en el objeto ES de js/i18n.js
          -> en español se verá ese texto en inglés.
- SOBRA:  la clave está en js/i18n.js o js/i18n-proyectos.js pero ya no se usa en ningún sitio (se puede borrar).
"""
import glob
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


js = leer(os.path.join(RAIZ, "js", "i18n.js"))
bloque = js[js.index("var ES = {"):js.index("// Textos que se usan desde JavaScript")]
claves_es = set(re.findall(r'^\s*"([\w-]+)":', bloque, re.M))
# traducciones de los proyectos generados con tools/construir.py
ruta_proy = os.path.join(RAIZ, "js", "i18n-proyectos.js")
if os.path.exists(ruta_proy):
    claves_es |= set(re.findall(r'^\s*"([\w-]+)":', leer(ruta_proy), re.M))

usadas = set()
paginas = glob.glob(os.path.join(RAIZ, "*.html")) + glob.glob(os.path.join(RAIZ, "proyectos", "*.html"))
paginas += glob.glob(os.path.join(RAIZ, "privado", "proyectos", "*.html"))
for ruta in paginas + [os.path.join(RAIZ, "tools", "proteger.py")]:
    usadas |= set(re.findall(r'data-i18n(?:-[\w-]+)?="([\w-]+)"', leer(ruta)))
usadas.discard("")

faltan = sorted(usadas - claves_es)
sobran = sorted(claves_es - usadas)

print(f"{len(usadas)} claves en uso, {len(claves_es)} traducciones en js/i18n.js")
if faltan:
    print("\nFALTA la traducción al español de:")
    for k in faltan:
        print("  -", k)
if sobran:
    print("\nSOBRA (no se usa en ningún sitio):")
    for k in sobran:
        print("  -", k)
if not faltan and not sobran:
    print("Todo en orden: cada clave tiene su traducción y no sobra ninguna.")
sys.exit(1 if faltan else 0)
