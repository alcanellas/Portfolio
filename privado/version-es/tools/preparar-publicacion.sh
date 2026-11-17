#!/bin/bash
# Crea una copia limpia del portfolio, lista para subir a Internet.
# Deja fuera todo lo que NO debe publicarse: privado/, tools/, documentación (.md) y archivos del sistema.
#
# Uso (desde la carpeta del portfolio):
#   bash tools/preparar-publicacion.sh                 # crea "../Portfolio ALC - publicar"
#   bash tools/preparar-publicacion.sh /ruta/destino   # crea la copia en otra carpeta
set -euo pipefail

ORIGEN="$(cd "$(dirname "$0")/.." && pwd)"
DESTINO="${1:-$ORIGEN/../Portfolio ALC - publicar}"

rm -rf "$DESTINO"
mkdir -p "$DESTINO"

rsync -a \
  --exclude 'privado/' \
  --exclude 'tools/' \
  --exclude '*.md' \
  --exclude '.gitignore' \
  --exclude '.DS_Store' \
  "$ORIGEN/" "$DESTINO/"

echo "Carpeta lista: $DESTINO"
echo
echo "Contenido:"
(cd "$DESTINO" && find . -type f | sort | sed 's|^\./|  |')
echo
# Comprobaciones de seguridad
if [ -d "$DESTINO/privado" ]; then echo "AVISO: ha quedado la carpeta privado/"; exit 1; fi
if grep -rIl "privado/" "$DESTINO" >/dev/null 2>&1; then
  echo "AVISO: algún archivo menciona privado/; revísalo antes de subir:"
  grep -rIl "privado/" "$DESTINO"
fi
# Enlaces a archivos que no existen (aparte de las imágenes opcionales de portada)
python3 - "$DESTINO" <<'EOF'
import os, re, sys
raiz = sys.argv[1]
faltan = []
for dp, _, fs in os.walk(raiz):
    for f in fs:
        if not f.endswith(".html"):
            continue
        ruta = os.path.join(dp, f)
        txt = open(ruta, encoding="utf-8").read()
        for m in re.findall(r'(?:src|href)="([^"#?:]+)(?:#[^"]*)?"', txt):
            if m.startswith(("http", "mailto")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(dp, m))):
                faltan.append((os.path.relpath(ruta, raiz), m))
if faltan:
    print("Archivos enlazados que no existen (se mostrará la portada de respaldo si es una imagen de portada):")
    for pagina, m in faltan:
        print("  ", pagina, "->", m)
else:
    print("Todos los enlaces y las imágenes existen.")
EOF
