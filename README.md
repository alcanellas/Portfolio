# Portfolio ALC

Portfolio web de Ana López Canellas (UX/UI). HTML, CSS y JS estáticos, sin dependencias ni instaladores: se ve abriendo `index.html` en el navegador y se publica subiendo una carpeta a cualquier alojamiento estático.

Última actualización: 2026-10-21. **La web es bilingüe inglés/español** con selector de idioma (ver "Idioma"). Carpeta de trabajo: `~/Desktop/Portfolio ALC` (ya no hay copia en OneDrive).

**Otros documentos**
- `GUIA.md`: cómo hacer las tareas habituales (cambiar un color, añadir un proyecto, preparar imágenes, comprobar accesibilidad).
- `PUBLICAR.md`: cómo subirlo a Internet y conectar tu dominio.
- `SKILLS.md`: registro de skills y referencias que se han ido pasando.

## Estructura

```
index.html                    Proyectos: portada y tarjetas de proyecto
sobre-mi.html                 Sobre mí: presentación con fotos, habilidades, fotografía de viajes, certificaciones y contacto
proyectos/*.html              Una página por proyecto (6). Se GENERAN desde fichas/ (menos marca blanca, hecha a mano)
fichas/                       Una ficha de texto por proyecto, plantillas y orden.txt (el orden en la web)
css/styles.css                Todos los estilos, ordenados por secciones (índice al principio)
js/i18n.js                    Idioma: traducciones al español, selector EN/ES y textos de JavaScript
js/i18n-proyectos.js          Traducciones de los proyectos (AUTOGENERADO por construir.py; no se edita)
js/main.js                    Año del pie, tema claro/oscuro, portadas de respaldo, copiar el correo, carrusel y diálogos, filtros de Inicio, fotos apiladas y carrusel de viajes
js/unlock.js                  Descifrado de proyectos protegidos con contraseña (sin uso ahora)
tools/proteger.py             Protege o desprotege proyectos con contraseña
tools/construir.py            Genera páginas de proyecto, tarjetas y enlaces Anterior/Siguiente desde las fichas
tools/nuevo-proyecto.py       Crea la ficha de un proyecto nuevo a partir de una plantilla
tools/preparar-publicacion.sh Crea una carpeta limpia, lista para subir
tools/comprobar-idiomas.py    Comprueba que cada texto tiene su traducción al español
assets/fonts/                 Raleway (títulos) e Inter (texto), alojadas en local
assets/img/                   Logos, portadas e imágenes de los proyectos (solo lo que se usa)
assets/img/viajes/            Fotos del carrusel de Sobre mí (viaje-01.jpg … viaje-20.jpg)
privado/                      Originales y material sin usar (NO publicar, ver .gitignore)
```

`privado/` contiene los originales de las capturas, `sin-usar/` (imágenes retiradas de las páginas) y `styles-antes-de-ordenar.css` (copia del CSS anterior). Nada de esa carpeta debe subirse.

## Idioma

La web tiene dos idiomas, **inglés y español**, con un selector **EN | ES** junto al botón de modo oscuro.

- **Inglés:** está escrito directamente en el HTML. Es el idioma por defecto, el que ven los buscadores y quien no tiene JavaScript.
- **Español:** está en `js/i18n.js`, en el objeto `ES`. Cada texto del HTML lleva una clave (`data-i18n="clave"`; para atributos, `data-i18n-alt`, `-aria-label`, `-content`, `-href`…) y su traducción se busca por esa clave.
- **Qué idioma se muestra:** el que la persona haya elegido (se guarda en `localStorage`); si no ha elegido, español si su navegador está en español y, si no, inglés. Se puede forzar con `?lang=es` o `?lang=en` al final de la dirección. Para cambiar el idioma por defecto, edita `DEFAULT` en `js/i18n.js`.
- **Textos que salen de JavaScript** (mensajes del botón de copiar, etiquetas del carrusel y de la página de contraseña) están en el objeto `JS` del mismo archivo, en los dos idiomas.
- **Comprobar que no falta ninguna traducción:** `python3 tools/comprobar-idiomas.py`.
- **La página de contraseña** (`tools/proteger.py`) y la etiqueta "Password protected" de la tarjeta también se traducen.

Estos documentos (README, GUIA, PUBLICAR) están en español y nombran las secciones en español; equivalencias con el inglés de la web:

| Español | Inglés |
|---|---|
| Proyectos / Sobre mí | Projects / About me |
| Descripción / En qué consistió / Herramientas | Description / What it involved / Tools |
| Estructura / Aplicación en proyectos | Structure / DS applied in projects |
| Escríbeme | Email me |
| Trabajo seleccionado | Selected work |

Criterios de la traducción al inglés: ortografía americana (*center*, *color*); los nombres de las certificaciones se han traducido de forma descriptiva (por ejemplo "Pruebas de accesibilidad con lector de pantalla NVDA" → "Accessibility testing with the NVDA screen reader"), así que si algún curso tiene un título oficial en inglés conviene sustituirlo; los títulos de los proyectos en inglés son nuevos ("Healthcare · Parenteral nutrition platform", etc.).

Copias de seguridad: `privado/version-es/` (la web entera en español, antes de ser bilingüe) y `privado/version-en/` (en inglés, antes del selector).

## Decisiones de diseño

- **Selector de idioma:** pieza de cristal EN | ES junto al botón de tema; en pantallas estrechas (menos de 700 px) la cabecera deja de ser simétrica y todo se reduce para que quepa hasta en 320 px.
- **Menú de dos secciones:** *Proyectos* (`index.html`) y *Sobre mí* (`sobre-mi.html`). Tu nombre solo aparece en Sobre mí.
- **Color:** escala morado-azulada `--c-50` a `--c-950` (#5A3155 a #DFEEF0) para acentos y detalles; neutros `--n-50` a `--n-950` para texto y superficies del modo oscuro. Se define en el bloque 1 de `css/styles.css`; es el único sitio donde hay que tocar un color.
- **Tema claro/oscuro:** sigue el ajuste del sistema (fondo blanco puro en claro, negro puro en oscuro). El botón de la cabecera lo cambia y guarda la elección en `localStorage`; mientras no haya elección guardada, si el sistema cambia, la web cambia con él. La lógica está en `js/main.js` (arriba del todo) y en el `<script>` de una línea del `<head>` de cada página (evita el parpadeo al cargar; `tools/construir.py` lo incluye en las páginas que genera). Para que la web entre siempre en oscuro habría que cambiar ambos sitios.
- **Liquid glass:** cabecera flotante en tres piezas (logo, menú, tema), etiquetas y candado de las portadas, aviso de confidencialidad y forma de la portada. Todo usa las variables `--glass-*` del bloque 1. Con "reducir transparencias" del sistema se vuelve de fondo sólido, y en alto contraste usa los colores del sistema.
- **Fondo:** cuaderno de puntos muy suave (propiedad `background-image` de `body`; se desactiva en alto contraste).
- **Portada de Inicio:** forma de cristal amorfa y animada (`.hero::before`). Se queda quieta con "reducir movimiento" y se oculta en móvil y en alto contraste.
- **Tipografía:** Raleway para títulos e Inter para texto, ambas en `assets/fonts/` (sin Google Fonts).
- **Esquinas redondeadas:** variables `--r-sm`, `--r-md`, `--r-lg`, `--r-pill`.
- **Logo de la cabecera:** `assets/img/logo-circular.png` (256 px). `logo-color.svg` es el favicon.
- **Confidencialidad:** ningún cliente se nombra; cada proyecto se presenta por sector y trabajo realizado. Las imágenes no deben llevar logos, marcas ni pantallas reales de clientes: se publican desenfocadas o anonimizadas.

## Accesibilidad

Objetivo WCAG AA. Incluye: enlace para saltar al contenido, foco visible, `prefers-reduced-motion`, `prefers-reduced-transparency`, modo de alto contraste (`forced-colors`), listas con `role`, `alt` vacío en imágenes decorativas y `aria-current` en el menú.

Contrastes calculados (mínimo 4,5:1 para texto normal):

| Pareja | Ratio |
|---|---|
| Texto `#241D23` sobre blanco | 16,5 |
| Texto secundario `#3D3A47` sobre blanco | 11,1 |
| Acento `#724B84` (etiquetas) sobre blanco | 6,9 |
| Botones: texto negro sobre `#7F7ABA` | 5,4 |
| Botón "Escríbeme": blanco sobre `#724B84` | 6,9 |
| Oscuro: texto `#D7DADB` sobre negro | 14,9 |
| Oscuro: texto secundario `#BDC1C2` sobre negro | 11,6 |
| Oscuro: acento sobre negro | 10,8 |

Con la paleta actual, el texto de los botones va en **negro**: el blanco sobre `#7F7ABA` no llega a 4,5:1. Si cambias la paleta, vuelve a calcular estas parejas (ver `GUIA.md`).

## Proyectos (orden en la web)

| Proyecto (título en inglés en la web) | Año | Página |
|---|---|---|
| Proyecto interno · Sistema de diseño de marca blanca (Internal project · White-label design system) | 2026 | `design-system-marca-blanca.html` |
| Sanidad · Plataforma de nutrición parenteral (Healthcare · Parenteral nutrition platform) | 2026 | `sanidad-nutricion-parenteral.html` |
| Seguros · Migración a AEM (Insurance · AEM migration) | 2025 | `seguros-migracion-aem.html` |
| Turismo · Accesibilidad en design system (Tourism · Accessibility in a design system) | 2025 | `turismo-accesibilidad.html` |
| Rediseño UX plataforma salud (Health platform UX redesign) | 2025 | `sanidad-app-interna.html` |
| E-commerce | 2024 | `retail-ecommerce.html` |

Todos muestran "Accenture Spain" como empresa. **Todo se cambia en la ficha** del proyecto (`fichas/<proyecto>.txt`) y se reconstruye con `python3 tools/construir.py`: la página, la tarjeta de Inicio y los enlaces *Anterior* y *Siguiente* (que van en círculo según `fichas/orden.txt`) se actualizan solos. Solo `design-system-marca-blanca` se edita a mano.

## Cómo se construyen los proyectos (fichas)

Cada proyecto tiene una **ficha de texto** en `fichas/` con sus datos en inglés y español. `python3 tools/construir.py` lee las fichas y genera:
- `proyectos/<proyecto>.html` (la página),
- la tarjeta del proyecto en `index.html`,
- los enlaces *Anterior/Siguiente* de todas las páginas de proyecto (también de las hechas a mano),
- `js/i18n-proyectos.js` con las traducciones al español.

Hay **dos tipos de proyecto**:
- **`confidencial`:** estructura **fija, siempre la misma**: portada con candado, *Description*, *What it involved*, *Tools*, y aviso de acuerdo de confidencialidad con el botón "Email me". No admite secciones extra (el script da error si se intenta), así que todos los confidenciales quedan iguales.
- **`abierto`:** estructura **configurable**: tras la cabecera y la portada se eligen las secciones, su orden y cuántas: texto, lista, herramientas, imagen, galería, carrusel, tarjetas, texto-imagen, cita, datos y enlace.

Plantillas con todos los campos explicados: `fichas/_plantilla-confidencial.txt` y `fichas/_plantilla-abierto.txt`. Para crear un proyecto: `python3 tools/nuevo-proyecto.py nombre confidencial|abierto`. Guía paso a paso en `GUIA.md`.

El script **no regenera** un proyecto que esté protegido con contraseña (te avisa) y deja intactas las páginas sin ficha. Las 5 páginas confidenciales actuales se generaron a partir de sus fichas y se comprobó que el resultado es idéntico al anterior píxel a píxel, en inglés y en español.

**Estructura de una página de proyecto confidencial:** cabecera (título, fecha, empresa, etiquetas), portada, Descripción, En qué consistió, Herramientas, aviso de confidencialidad (proyectos de cliente) y Anterior/Siguiente.

**Proyecto de marca blanca** (interno, hecho a mano, sin ficha, sin aviso de confidencialidad ni candado): además lleva *Estructura* (3 tarjetas, una por archivo de Figma), *Workshops* (texto e imagen pendientes) y *Aplicación en proyectos* (dos tarjetas, *Adaptación a app* y *Adaptación a web*, que abren un carrusel de pantallas).

## Filtros de proyectos (Inicio)

Encima de las tarjetas hay un menú de filtros por **empresa**, **año** y **tipo de cliente**. A partir de 1400 px de ancho es un menú lateral a la izquierda (se queda fijo al hacer scroll); en pantallas más estrechas pasa a ser una fila de pills encima de las tarjetas. Los filtros se combinan entre sí, se pueden quitar volviendo a pulsarlos y "Todos los proyectos" los limpia.

- Se crean solos (en `js/main.js`) a partir de los `data-company`, `data-year` y `data-sector` de cada tarjeta, así que un proyecto nuevo aparece en el menú sin tocar nada más.
- `empresa` y `anio` ya estaban en la ficha. El **tipo de cliente** es el campo nuevo `sector_en` / `sector_es` (por ejemplo `Healthcare` / `Sanidad`). Usa exactamente el mismo texto en todos los proyectos del mismo sector, o saldrán como dos filtros distintos. Está en las plantillas.
- El proyecto de marca blanca (hecho a mano) lleva esos datos directamente en su `<a class="card">` de `index.html`.
- Los textos del menú y de los avisos están en el objeto `JS` de `js/i18n.js` (claves `filter…`, `f…`).

## Portadas e imágenes

Cada tarjeta y cada página de proyecto carga `assets/img/<proyecto>.jpg` (el nombre del HTML sin `.html`). Las portadas son capturas **recortadas a 16:10** (1600 × 1000 px) y alineadas arriba: se ve la parte superior de la pantalla, no entera. Si el archivo no existe, se muestra automáticamente una portada de respaldo (patrón diagonal, candado y etiqueta), sin tocar código.

Los proyectos de cliente llevan candado sobre la portada (clase `cover-keep-lock`); el de marca blanca no.

- **Texto alternativo (alt):** cada imagen lleva un `alt` que describe lo que se ve. Las portadas de las tarjetas llevan `alt=""` a propósito: son decorativas y el título de la tarjeta ya da el nombre.
- **Aplicación en proyectos (marca blanca):** `design-system-marca-blanca-aplicacion-1.png` a `-7.png`. Las del proyecto web (4 a 7) llevan logotipos y textos desenfocados.
- **Imágenes para modo claro y oscuro:** una imagen puede tener versión clara (`nombre.png`) y oscura (`nombre-dark.png`). Usa en su `<figure>` la clase `theme-pair` y dos `<img>` con las clases `img-light` e `img-dark`. Ahora mismo ninguna imagen usa este recurso.
- **Workshops:** `assets/img/design-system-marca-blanca-workshops.jpg` (1200 × 750 px, recortada de la foto original `assets/img/workshop.jpeg`).
- Cómo preparar una captura: ver `GUIA.md`.

## Sobre mí: fotos apiladas

Dos fotos con las esquinas redondeadas, sin marco, superpuestas y sujetas con un **imán de cristal morado** con la forma de la bola de la portada (`.print::after`). La del sillón va delante y arriba; la de la Gran Muralla va detrás, más baja y casi tapada. Al pasar el ratón por la de atrás (o tocarla en móvil) pasa delante; al sacar el ratón vuelve a su sitio (`js/main.js`, bloque "Sobre mí: fotos apiladas").

- **Archivos:** `assets/img/sobre-mi-1.jpg` (delante) y `assets/img/sobre-mi-2.jpg` (detrás). Para cambiarlas, sustituye el archivo por otro con el mismo nombre (vertical, 3:4 o más alto, unos 900-1200 px de ancho) y actualiza su texto alternativo (el `alt` en `sobre-mi.html` y la clave `portrait_armchair` / `portrait_great_wall` en `js/i18n.js`). Los originales están en `privado/`.
- **Encuadre:** las imágenes se recortan a 3:4 (`object-fit: cover`). La de atrás usa `.print.is-back img { object-position: 50% 42% }`; cambia ese porcentaje para subir o bajar el recorte.
- **Colocación:** variables sueltas en las reglas `.prints`, `.print.is-front` y `.print.is-back` (`left/right/top`, `rotate`, anchura `width`). El tamaño del conjunto es `max-width` de `.prints` y la primera columna de `.about` (hoy 500 px y 480 px).
- **Imanes:** `.print::after`, con el mismo degradado de la bola pero **opaco** (usa `--c-500`/`--c-700`; en oscuro `--c-300`/`--c-500`). El de la foto de atrás está a la derecha para que no lo tape la de delante.
- Las habilidades (pills) van **debajo del texto**, en la segunda columna.

## Sobre mí: fotografía de viajes

Tira de 20 fotos a todo el ancho de la pantalla, en movimiento continuo y en bucle (sección `#viajes` de `sobre-mi.html`, estilos `.marquee*` al final de `css/styles.css`, código en `js/main.js`, bloque "Fotografía de viajes").

- **Cómo funciona:** el HTML tiene una sola lista `<ul class="marquee-set">` con las fotos. `js/main.js` la **duplica** (la copia lleva `aria-hidden` y `alt` vacío, para que los lectores de pantalla no lean las fotos dos veces) y la anima con `@keyframes marquee` (de 0 a -50 %), así el bucle no tiene saltos.
- **Velocidad:** `animation: marquee 110s` en `.marquee-track`. Cuanto mayor el número, más lento. Si añades o quitas fotos, ajusta ese número para mantener una velocidad parecida (hoy unos 60 px/s con 20 fotos; regla práctica: 5,5 s por foto).
- **Accesibilidad:** se pausa al pasar el ratón o al enfocar con el teclado, y hay un botón de pausa/reanudar arriba a la derecha de la sección (textos `pauseCarousel` y `playCarousel` en el objeto `JS` de `js/i18n.js`). Con "reducir movimiento" no se anima: queda una fila con scroll horizontal. Sin JavaScript también queda esa fila.
- **Fotos:** `assets/img/viajes/viaje-NN.jpg`, a 800 px de alto (la altura en pantalla es 320 px, o 220 en móvil). Los originales están en `privado/viajes-originales/`. El orden es el del HTML.
- **Textos alternativos:** cada foto lleva `alt` en inglés (en el HTML) y en español (claves `trip_01` … `trip_20` en `js/i18n.js`). Pasos para añadir o quitar fotos: `GUIA.md`, punto 5.
- Las fotos 05 a 12 se describen en el `alt` como "Film photo" (foto analógica) a partir de cómo se ven, no porque lo hayas confirmado: revisa cuáles son realmente analógicas.

## Aviso de acuerdo de confidencialidad

Los 5 proyectos de cliente llevan, bajo *En qué consistió* y *Herramientas*, una tarjeta de cristal: "Project protected by a confidentiality agreement" y el botón **Email me** (Escríbeme). El botón abre la app de correo con un mensaje nuevo a tu dirección y el nombre del proyecto como asunto (`mailto:`). Si la persona no tiene app de correo configurada, el botón no hace nada; para eso está el botón de copiar el correo en *Sobre mí → Contacto*.

## Proyectos protegidos con contraseña

Preparado, pero **ahora mismo ningún proyecto está protegido**. El script `tools/proteger.py` cifra el contenido de una página de proyecto (AES-256 + PBKDF2) y `js/unlock.js` lo descifra en el navegador al introducir la contraseña. No necesita instalar nada (solo Python 3 y openssl, que vienen con macOS).

```
python3 tools/proteger.py estado                      # ver qué proyectos están protegidos
python3 tools/proteger.py proteger retail-ecommerce   # pide la contraseña (mínimo 12 caracteres)
python3 tools/proteger.py quitar retail-ecommerce     # vuelve a dejarlo público
```

- El original sin cifrar se guarda en `privado/proyectos/`. Edita siempre ahí y vuelve a ejecutar `proteger`. **No subas `privado/`**.
- Solo se cifra el texto de la página. Las imágenes son archivos normales y accesibles por su dirección: usa solo imágenes anonimizadas, o protección a nivel de hosting si necesitas más.
- La tarjeta de la portada cambia su etiqueta a "Protegido con contraseña" y la página lleva `noindex`.
- El cifrado es tan fuerte como la contraseña: usa una frase larga (4 palabras al azar).
- Una vez desbloqueado, no se vuelve a pedir en esa pestaña del navegador.

## Pendiente

**Contenido**
- Sección *Workshops* (marca blanca): confirmar el texto de la Sesión 2 y la frase final ("The aim was…"), que escribí por mi cuenta sin que me los dieras: solo la Sesión 1 viene de lo que me contaste.
- Revisar la traducción al inglés y la al español (sobre todo los títulos de las certificaciones y el texto de Sobre mí) con alguien nativo o con un revisor.
- Probar la página de contraseña ya traducida si algún día se protege un proyecto: el descifrado en el navegador no se ha podido probar con la traducción.
- Revisar los datos de las 3 tarjetas de *Estructura* (marca blanca): "17 componentes", "flujo de registro de 12 pantallas" y el nombre del equipo interno ("EMEA ATC"). Confirmar que se pueden publicar.
- El título del proyecto de marca blanca ("Proyecto interno · Sistema de diseño de marca blanca") quizá ya no encaja con su contenido.
- Ampliar *Sobre mí* si quieres más texto.
- Confirmar los **textos alternativos de las fotos de viajes** (`trip_01`…`trip_20`): solo nombran un lugar cuando se lee en la foto o es inconfundible (Gran Muralla, Berlín, Las Vegas, Seattle, Empire State, Parlamento de Hungría); en el resto se describe lo que se ve. Si quieres nombrar los sitios, cámbialos en el HTML y en `js/i18n.js`.
- Probar en móvil real las fotos apiladas (cambio al tocar) y el carrusel de viajes; no se han podido comprobar por debajo de 500 px de ancho.
- Comprobar el carrusel en movimiento en un navegador normal (las capturas sin ventana no ejecutan bien la animación; el bucle sí se verificó).
- Logos para WCAG (por ejemplo el de W3C) en las herramientas del proyecto de Turismo.
- El encabezado de la lista en Inicio dice "Selected work"; valorar "Selected projects" para que coincida con el menú.
- Certificaciones: si hay más, añadirlas en `sobre-mi.html` (id `certificaciones`); valorar agrupar las de weAAAre si la lista crece.

**Antes de publicar**
- Revisar con WAVE o Lighthouse y navegar solo con teclado (ver `GUIA.md`).
- Probar en un móvil real: el menú, la tarjeta de confidencialidad y la forma de la portada no se han podido comprobar por debajo de 500 px de ancho.
- Revisar con el equipo si hace falta aprobación interna antes de publicar los proyectos.
- Decidir si algún proyecto se protege con contraseña.
- Elegir dónde publicar y dominio (ver `PUBLICAR.md`). Considerar un correo solo para el portfolio en lugar del personal, que ahora está visible en Sobre mí y en los botones de los proyectos.

## Referencias de inspiración

robhope.com, billysweeney.com, whyramachandran.design, junhyungpark.com, jaykay-design.com, marinaredondo.com, liumichelle.com
