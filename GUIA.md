# Guía de tareas habituales

> La web es bilingüe (inglés en el HTML, español en `js/i18n.js`). Estas guías están en español y nombran las secciones en español (equivalencias en `README.md → Idioma`).

Todo se edita con un editor de texto (por ejemplo TextEdit en modo "texto sin formato", o el que prefieras). Después de cambiar algo, abre `index.html` en el navegador y **recarga sin caché** (⌘ + Mayús + R) para ver el cambio.

## 0. El mapa en 30 segundos

| Quiero… | Qué hago |
|---|---|
| Cambiar el texto de un proyecto de cliente o de un proyecto abierto | Edito su **ficha** `fichas/<proyecto>.txt` y ejecuto `python3 tools/construir.py` |
| Añadir un proyecto | `python3 tools/nuevo-proyecto.py nombre confidencial` (o `abierto`), edito la ficha y construyo |
| Cambiar el orden de los proyectos | Cambio el orden de las líneas de `fichas/orden.txt` y construyo |
| Cambiar un color | Bloque 1 de `css/styles.css` (punto 2 de esta guía) |
| Cambiar Sobre mí, certificaciones, contacto o la portada de Inicio | Edito `sobre-mi.html` / `index.html` y su traducción en `js/i18n.js` (punto 1) |
| Cambiar las fotos apiladas de Sobre mí o añadir/quitar fotos de viajes | Punto 5 de esta guía |
| Comprobar que no falta ninguna traducción | `python3 tools/comprobar-idiomas.py` |
| Subirlo a Internet | `bash tools/preparar-publicacion.sh` y subo la carpeta que crea (ver `PUBLICAR.md`) |

**Regla de oro:** las páginas de proyecto (menos `design-system-marca-blanca`), las tarjetas de Inicio, los enlaces Anterior/Siguiente y `js/i18n-proyectos.js` **se generan**: no se editan a mano, porque `construir.py` los reescribe. Se cambian desde las fichas.

## 1. Cambiar un texto (en los dos idiomas)

**En una ficha de proyecto**, cada texto tiene su versión `_en` (inglés) y `_es` (español) en el mismo archivo. Basta con editar los dos y construir.

**En las páginas hechas a mano** (`index.html`, `sobre-mi.html` y `proyectos/design-system-marca-blanca.html`) cada texto existe en dos sitios:
1. **Inglés:** en el HTML (el texto que ves en la etiqueta).
2. **Español:** en `js/i18n.js`, objeto `ES`, buscando la clave que lleva esa etiqueta (`data-i18n="clave"`; si es un atributo, `data-i18n-alt="clave"`, etc.).

Para un texto **nuevo** en esas páginas: añade `data-i18n="mi_clave"` a la etiqueta del HTML (si la etiqueta mezcla texto y otras etiquetas, envuelve solo el texto en `<span data-i18n="mi_clave">…</span>`), y añade `"mi_clave": "Texto en español",` al objeto `ES`. Después ejecuta `python3 tools/comprobar-idiomas.py` para ver si falta o sobra algo. Para probar el español: `index.html?lang=es`.

Dónde está cada cosa:

- **Presentación, fotos, habilidades, fotografía de viajes, certificaciones y contacto:** `sobre-mi.html`.
- **Titular y aviso de la portada:** `index.html`.
- **Texto de un proyecto:** su ficha en `fichas/`. (El proyecto de marca blanca, que es especial, se edita en `proyectos/design-system-marca-blanca.html`.)
- **El texto del aviso de confidencialidad, los títulos "Description / What it involved / Tools":** son comunes a todos los proyectos: se cambian en `js/i18n.js` (español) y en `tools/construir.py` (inglés).

## 2. Cambiar un color

Los colores están en el **bloque 1** de `css/styles.css` (el primero, "Variables"). La escala `--c-50` a `--c-950` es la paleta de acento; `--n-50` a `--n-950`, los neutros. No hay colores sueltos por el resto del archivo.

Después de cambiar la paleta, **vuelve a comprobar el contraste** del texto (mínimo 4,5:1). Con Python (viene con macOS) puedes calcular una pareja:

```
python3 - <<'EOF'
def lum(h):
    h = h.lstrip('#'); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda v: v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def contraste(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
print(round(contraste('#000000', '#7F7ABA'), 2))   # texto de botón sobre su fondo
EOF
```

Parejas a revisar: texto de los botones sobre `--btn-bg`, el acento (`--accent`) sobre blanco y sobre negro, y el texto sobre la forma de la portada. Si el texto negro de los botones deja de llegar a 4,5:1, cambia `--btn-text` a `#FFFFFF` (en los dos modos) o aclara/oscurece el fondo del botón.

## 3. Proyectos: fichas, tipos y secciones

Los proyectos viven en **fichas** de texto (`fichas/<proyecto>.txt`). El script `tools/construir.py` las convierte en la página del proyecto, la tarjeta de Inicio, los enlaces Anterior/Siguiente y las traducciones.

### Añadir un proyecto nuevo

1. Crea la ficha: `python3 tools/nuevo-proyecto.py banca-app confidencial` (o `abierto`). Copia la plantilla a `fichas/banca-app.txt` y lo pone el primero de `fichas/orden.txt`.
2. Abre `fichas/banca-app.txt` y rellénala (las plantillas explican cada campo en los comentarios).
3. Sube la portada a `assets/img/banca-app.jpg` (punto 4).
4. Ejecuta `python3 tools/construir.py`. Si algo está mal, el script te dice en qué línea y qué falta.
5. Abre `index.html` y la página nueva en el navegador. Prueba también `?lang=es`.
6. Añade la fila a la tabla de proyectos de `README.md` (opcional, es documentación).

### Los dos tipos de proyecto

- **`tipo: confidencial`**: estructura **fija, siempre igual**. Portada con candado y etiqueta "Confidential client", *Description*, *What it involved*, *Tools* y el aviso de acuerdo de confidencialidad con el botón "Email me" (asunto = título del proyecto). No admite secciones extra; si intentas añadirlas, el script da error. Así todos los proyectos confidenciales se ven igual.
- **`tipo: abierto`**: estructura **configurable**. Cabecera y portada fijas, y después **tú eliges las secciones**, su orden y cuántas (copia/pega/borra bloques `[seccion ...]`).

### Secciones de un proyecto abierto

| Sección | Para qué sirve | Opciones |
|---|---|---|
| `[seccion texto]` | Título + párrafos | `ancho: completo` o `mitad` |
| `[seccion lista]` | Título + viñetas | `ancho: completo` o `mitad` |
| `[seccion herramientas]` | Logos y nombres de herramientas | — |
| `[seccion imagen]` | Una imagen con pie | `ajuste: entera` o `recortada` |
| `[seccion galeria]` | Varias imágenes en 2 o 3 columnas | `columnas: 2` o `3`; `[[imagen]]` repetido |
| `[seccion carrusel]` | Imágenes que se deslizan | `[[diapositiva]]` repetido |
| `[seccion tarjetas]` | Tarjetas con etiqueta, título y texto | `[[tarjeta]]` repetido |
| `[seccion texto-imagen]` | Texto a un lado e imagen al otro | `lado: derecha` o `izquierda` |
| `[seccion cita]` | Una frase destacada | autor opcional |
| `[seccion datos]` | Cifras clave | `[[dato]]` repetido |
| `[seccion enlace]` | Botón que abre una web | `url` |

Las secciones `texto` y `lista` con `ancho: mitad` que van seguidas se colocan lado a lado (como *Description* y *What it involved*). `_plantilla-abierto.txt` tiene un ejemplo de cada una.

### Formato de las fichas

- `#` al principio de una línea = comentario. Al final de una línea, ` # comentario` (con dos espacios antes) también.
- Todo texto va en dos idiomas: `titulo_en` / `titulo_es`, `texto_en` / `texto_es`…
- Texto de varias líneas: `campo: |` y las líneas siguientes con 2 espacios de sangría; una línea en blanco separa párrafos.
- Listas: una línea por elemento empezando por `- ` (los mismos elementos en inglés y en español).
- Herramientas con logo automático: Figma, Figma Make, Claude Code, Jira, Atlassian, VoiceOver (iOS). Otras con logo propio: `Nombre|archivo.svg` (archivo en `assets/img/`).
- Si falta un texto en español, el script avisa y en español se verá el inglés.

### Cambiar el orden de los proyectos

Edita `fichas/orden.txt` (de arriba abajo = el orden en la web) y ejecuta `python3 tools/construir.py`: se reordenan las tarjetas y se recalculan los enlaces Anterior/Siguiente de todas las páginas.

### Quitar un proyecto

Borra su línea de `fichas/orden.txt` y, si quieres, su ficha y `proyectos/<proyecto>.html`. Ejecuta `python3 tools/construir.py`.

### Proyectos con contraseña

`tools/proteger.py` cifra una página ya construida. Mientras un proyecto esté protegido, `construir.py` **no lo regenera** (te avisa): ejecuta antes `python3 tools/proteger.py quitar <proyecto>`, construye y vuelve a proteger.

### El proyecto de marca blanca

`design-system-marca-blanca.html` es una página hecha a mano (tiene diálogos con carrusel y otras piezas especiales). No tiene ficha: se edita directamente en su HTML y sus traducciones en `js/i18n.js`. `construir.py` solo actualiza su tarjeta y sus enlaces Anterior/Siguiente.

## 4. Preparar una imagen

Las portadas son capturas **recortadas a 16:10**, de 1600 × 1000 px, en JPEG. En macOS se puede hacer con `sips` (viene instalado). Dos pasos: recortar y convertir.

```
# 1) Recortar a proporción 16:10 desde la esquina superior izquierda.
#    -c ALTO ANCHO   --cropOffset DESPLAZAMIENTO_VERTICAL DESPLAZAMIENTO_HORIZONTAL
sips -c 780 1248 --cropOffset 14 36 captura.png --out recorte.png

# 2) Pasar a 1600 px de ancho y a JPEG ligero
sips --resampleWidth 1600 -s format jpeg -s formatOptions 82 recorte.png --out assets/img/mi-proyecto.jpg
```

- Para saber las medidas de una captura: `sips -g pixelWidth -g pixelHeight captura.png`.
- Quita unos 30 px de los bordes si la captura trae esquinas redondeadas o sombra.
- **Un archivo con extensión `.jpg` puede ser en realidad un PNG o un PDF.** Compruébalo con `file archivo.jpg`. Si dice PDF o PNG, conviértelo con `sips -s format jpeg entrada --out salida.jpg`.
- Guarda siempre el original en `privado/` y publica solo la versión recortada, anonimizada y sin datos reales de clientes.
- Escribe un `alt` que explique qué se ve y qué aporta (no "imagen del proyecto").

## 5. Fotos de Sobre mí y fotografía de viajes

### Cambiar una de las dos fotos apiladas

1. Prepara la foto (vertical, unos 900-1200 px de ancho):
   ```
   sips -Z 1400 -s format jpeg -s formatOptions 82 mi-foto.jpeg --out assets/img/sobre-mi-1.jpg
   ```
   (`sobre-mi-1.jpg` va delante; `sobre-mi-2.jpg` va detrás.) Guarda el original en `privado/`.
2. Si cambian las medidas, actualiza `width` y `height` del `<img>` en `sobre-mi.html`.
3. Actualiza el texto alternativo: el `alt` del HTML (inglés) y su clave en `js/i18n.js` (`portrait_armchair` o `portrait_great_wall`, español).
4. Si la cara queda cortada, cambia el recorte: `object-position` en `.print img` (para la foto de atrás, `.print.is-back img`).

Posiciones, rotaciones, tamaño e imanes: `README.md → Sobre mí: fotos apiladas`.

### Añadir una foto de viajes

1. Reduce la foto a 800 px de alto y conviértela a JPEG (con el siguiente número libre, por ejemplo `viaje-21.jpg`):
   ```
   sips --resampleHeight 800 -s format jpeg -s formatOptions 80 original.jpeg --out assets/img/viajes/viaje-21.jpg
   sips -g pixelWidth -g pixelHeight assets/img/viajes/viaje-21.jpg     # para anotar el ancho y el alto
   ```
   Guarda el original en `privado/viajes-originales/`.
2. En `sobre-mi.html`, dentro de `<ul class="marquee-set">`, copia una línea `<li>…</li>` y cámbiale `src`, `alt` (inglés), `width`, `height` y `data-i18n-alt="trip_21"`. **El orden de las líneas es el orden en la web.**
3. En `js/i18n.js`, objeto `ES`, añade `"trip_21": "Descripción en español",` junto a las otras `trip_`.
4. Ejecuta `python3 tools/comprobar-idiomas.py` y recarga la página.
5. Si añades muchas, sube un poco el número de segundos de `animation: marquee 110s` (`.marquee-track` en `css/styles.css`) para que no vaya más rápido: unos 5,5 s por foto.

El `alt` debe describir lo que se ve (y el lugar solo si estás segura de cuál es). Para quitar una foto, borra su línea `<li>` y su clave `trip_NN` de `js/i18n.js`; no hace falta renumerar.

### Cambiar el carrusel

- **Velocidad:** `animation: marquee 110s` en `.marquee-track` (más segundos = más lento).
- **Tamaño de las fotos:** `height: 320px` en `.marquee-set img` (y `220px` en el `@media (max-width: 760px)`).
- **Dirección:** para que vaya hacia la derecha, intercambia `from` y `to` en `@keyframes marquee`.
- **Pausa:** el botón y la pausa al pasar el ratón están en `css/styles.css` (`.marquee-toggle`, `.marquee.is-moving:hover …`) y en `js/main.js`.
- **Título de la sección:** clave `travel_photography` en `js/i18n.js` y el `<h2>` de `sobre-mi.html`.

## 6. El aviso de confidencialidad

Lo genera `construir.py` en todos los proyectos `tipo: confidencial`, con el mismo texto y estructura. El botón "Email me" abre un correo a `alcanellass@gmail.com` con el título del proyecto como asunto. Para cambiar la dirección de correo: `CORREO` al principio de `tools/construir.py` y el de `sobre-mi.html`. Para cambiar el texto: `tools/construir.py` (inglés) y `js/i18n.js` (español, claves `project_protected_by_a_confidentiality_agreement` y `get_in_touch_if_you_would`).

## 7. Cambiar el aspecto del cristal, el fondo o la forma de la portada

- **Cristal:** variables `--glass-*` del bloque 1. `--glass-blur` controla el desenfoque.
- **Fondo de puntos:** regla `body` del bloque 2 (`background-size` es la separación; el `14%` la intensidad).
- **Forma de la portada:** `.hero::before` y `@keyframes blob` en el bloque 4. La duración de la animación es `14s`.

## 8. Comprobar accesibilidad

- **Teclado:** pulsa Tab desde el principio de cada página. Debe verse siempre dónde está el foco, el orden debe ser lógico y todo debe poder usarse sin ratón (menú, botón de tema, tarjetas, botón de copiar, carrusel, diálogo).
- **Lighthouse:** en Chrome, clic derecho → Inspeccionar → pestaña *Lighthouse* → marca *Accessibility* → *Analyze page load*. Objetivo: 100, o ver qué falla.
- **WAVE:** extensión de Chrome (wave.webaim.org). Revisa errores y alertas de contraste.
- **Lector de pantalla:** prueba al menos una página con VoiceOver (⌘ + F5).
- **Ajustes del sistema:** prueba "Reducir movimiento", "Reducir transparencia" y "Aumentar contraste" (Ajustes del Sistema → Accesibilidad → Pantalla).
- **Zoom:** haz zoom al 200 % y comprueba que nada se corta.

## 9. Probar en móvil

- En Chrome: Inspeccionar → icono de móvil (barra superior de la herramienta) y elige un modelo.
- Lo ideal es abrirlo en un móvil real una vez publicado. Cosas a mirar: cabecera (logo, menú y tema caben), tarjeta de confidencialidad, botones táctiles de al menos 44 px.

## 10. Capturas para revisar (opcional)

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --screenshot=captura.png --window-size=1280,900 "file://$PWD/index.html"
```

Añade `--force-dark-mode` para ver el modo oscuro. Las capturas sin ventana no ejecutan bien las animaciones: la tira de viajes aparece casi quieta; para verla moverse, abre la página en el navegador.

## 11. Problemas frecuentes

| Síntoma | Causa y solución |
|---|---|
| El cambio no se ve | Recarga sin caché (⌘ + Mayús + R). |
| Un texto sigue en inglés al elegir español | Falta su traducción: ejecuta `python3 tools/comprobar-idiomas.py`. |
| Cambié el texto en inglés y en español sigue el antiguo | La traducción vive en `js/i18n.js`; cámbiala allí también. |
| Una imagen no aparece | Nombre o extensión distinta, o archivo que en realidad es otro formato (`file archivo`). |
| Aparece la portada morada con candado | No existe `assets/img/<proyecto>.jpg`. Es el comportamiento de respaldo. |
| El botón "Email me" no hace nada | La persona no tiene una app de correo configurada. Tiene el botón de copiar en *Sobre mí*. |
| Un enlace Anterior/Siguiente falla | Ejecuta `python3 tools/construir.py`: los recalcula todos. |
| `construir.py` da un ERROR | Lee el mensaje: dice la ficha, la línea y qué falta (por ejemplo un `_es`, una lista con distinto número de elementos o un nombre de archivo mal escrito). |
| Edité una página generada y mi cambio desapareció | Se regeneró al construir. Haz el cambio en la ficha. |
| La forma de la portada o el carrusel de viajes no se mueven | Tienes activado "Reducir movimiento" en el sistema. Es lo esperado (el carrusel queda como una fila con scroll). |
| La web sale en claro/oscuro y no esperaba | Sigue el ajuste del sistema, salvo que hayas pulsado el botón de tema (se guarda). Para borrar la elección: borrar datos del sitio, o en la consola `localStorage.removeItem('theme')`. |
| Una foto del carrusel se ve distorsionada o falta | Revisa `width`/`height` del `<img>` y que el archivo exista en `assets/img/viajes/`. |

## 12. Qué no tocar sin cuidado

- `privado/`: originales y material interno. No se publica.
- `js/unlock.js` y `tools/proteger.py`: forman la protección con contraseña; se usan juntos.
- Los bloques `@media (prefers-...)` y `forced-colors` al final de `css/styles.css`: son los ajustes de accesibilidad.
- `proyectos/*.html` (excepto marca blanca), las tarjetas de `index.html` y `js/i18n-proyectos.js`: los reescribe `tools/construir.py`; edita las fichas en su lugar.
