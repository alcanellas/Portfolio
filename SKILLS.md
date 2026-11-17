# Skills para el portfolio

Registro de skills y referencias que Ana me pasa para tenerlas en cuenta al diseñar y modificar el portfolio.
Antes de tocar `index.html`, `css/` o `js/`, consultar este archivo y aplicar las skills listadas.

Cómo añadir una nueva: copiar la plantilla del final y rellenarla.

Actualizado: 2026-10-19. Carpeta de trabajo: `~/Desktop/Portfolio ALC`. Estado general en `README.md`.

---

## 1. taste-skill (Leonxlnx)

- **Comando indicado:** `npx skills add Leonxlnx/taste-skill`
- **Repositorio:** https://github.com/Leonxlnx/taste-skill
- **Web:** https://tasteskill.dev
- **Licencia:** MIT
- **Estado:** registrada; sin instalar (no se ha ejecutado el comando todavía)
- **Fecha:** 2026-10-19

**Qué hace:** dirección de arte "anti-slop" para frontends: landing pages, portfolios, páginas de producto, dashboards. Sirve para builds nuevos, rediseños y revisiones.

**Skill principal:** `design-taste-frontend`
Instalación recomendada, solo la skill principal:
`npx skills add https://github.com/Leonxlnx/taste-skill --skill "design-taste-frontend"`
Sin `--skill`, el comando original también instala las skills "classic" (opt-in, solo se ejecutan si se invocan por su nombre).

**Cómo trabaja (v2):**
1. Lee el brief y lista lo que solo tiene este cliente.
2. Un script propone 3 de 20 direcciones de diseño y se elige una.
3. Define la idea en una frase que une el material propio con esa dirección.
4. Construye con imágenes reales de colecciones abiertas, con crédito.
5. Revisa la página en un navegador real a 3 anchos y la suspende si detecta "slop".
6. Revisa sus capturas y corrige los 3 mayores problemas, hasta 3 rondas.

**Requisitos:** Node 22+ y Chrome, Edge o Chromium. No necesita API keys. Necesita red para buscar imágenes.

**Skills classic** (solo si se piden por nombre): `high-end-visual-design`, `minimalist-ui`, `industrial-brutalist-ui`, `gpt-taste`, `stitch-design-taste`.

**Cómo aplicarla en este portfolio:**
- Mantener la restricción de confidencialidad: nunca nombrar clientes ni usar imágenes con marcas o pantallas reales. Esto prevalece sobre las imágenes de stock o la inspiración de la skill.
- Referencias visuales ya acordadas: robhope.com, billysweeney.com, whyramachandran.design, junhyungpark.com, jaykay-design.com.
- Antes de aplicar cambios grandes de dirección visual, confirmar con Ana.

---

## 2. web-design-guidelines (Vercel Labs)

- **Comando indicado:** `npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines`
- **Repositorio:** https://github.com/vercel-labs/agent-skills (carpeta `skills/web-design-guidelines`)
- **Reglas fuente:** https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
- **Estado:** registrada; sin instalar (no se ha ejecutado el comando)
- **Fecha:** 2026-10-19

**Qué hace:** revisa código de UI frente a las Web Interface Guidelines de Vercel (accesibilidad, UX, buenas prácticas). Se activa con peticiones como "revisa mi UI", "audita el diseño" o "comprueba accesibilidad". Descarga las reglas actualizadas en cada revisión y devuelve los hallazgos en formato `archivo:línea`.

**Cómo aplicarla en este portfolio:**
- Es una skill de revisión, no de creación: usarla al terminar cada cambio importante sobre `index.html`, `css/styles.css` y `js/main.js`.
- Complementa a taste-skill: taste-skill define la dirección visual; esta audita el resultado.
- Requiere acceso a red para descargar las reglas.
- 2026-10-19: aplicada manualmente (sin instalar) como auditoría de accesibilidad de `index.html`, `proyectos/*.html` y `css/styles.css`. Reglas leídas de la URL fuente.

---

## 3. awesome-design-md (VoltAgent)

- **Enlace indicado:** https://github.com/VoltAgent/awesome-design-md.git
- **Tipo:** colección de referencia, no es una skill instalable con `npx`
- **Catálogo:** https://getdesign.md (cada entrada en `getdesign.md/<sitio>/design-md`)
- **Estado:** registrada; no se ha descargado ni clonado nada
- **Fecha:** 2026-10-19

**Qué es:** colección de unos 84 archivos `DESIGN.md` extraídos de webs reales (Claude, Cursor, Runway, Mistral, etc.). Un `DESIGN.md` es un documento de sistema de diseño en texto plano (tokens, patrones, reglas) que los agentes leen para generar UI coherente. Concepto introducido por Google Stitch. También permite solicitar un `DESIGN.md` de una web concreta en https://getdesign.md/request.

**Cómo aplicarla en este portfolio:**
- Idea de trabajo: crear un `DESIGN.md` propio del portfolio, con la paleta crema/naranja, la tipografía Inter Tight, el espaciado y las reglas, en la raíz de esta carpeta, y consultarlo en cada cambio visual para mantener la coherencia.
- Si Ana elige una web de la colección como referencia, leer su `DESIGN.md` en getdesign.md y extraer solo tokens y patrones, sin copiar marca ni contenido.
- Las referencias del catálogo son de productos para desarrolladores. Para un portfolio de diseño, las ya acordadas (robhope, billysweeney, whyramachandran, junhyungpark, jaykay-design) tienen prioridad.

---

## 4. image-to-code (Leonxlnx / imagegen-skills)

- **Comando indicado:** `npx skills add https://github.com/Leonxlnx/imagegen-skills --skill "image-to-code"`
- **Repositorio:** https://github.com/Leonxlnx/imagegen-skills (carpeta `skills/image-to-code`)
- **Estado:** registrada; sin instalar (no se ha ejecutado el comando)
- **Fecha:** 2026-10-19

**Qué hace:** pipeline "imagen primero": genera imágenes de diseño de la web por secciones, las analiza a fondo y después construye el frontend para igualarlas. Pensada para landings, páginas editoriales y portfolios. Evita los defectos típicos: una sola imagen comprimida para muchas secciones, texto ilegible, tarjetas dentro de tarjetas, hero cargado.

**Requisito clave:** necesita un agente que pueda generar imágenes además de escribir código. Claude Code no genera imágenes por sí solo, así que esta skill solo se podría aplicar de forma completa si se dispone de una herramienta de imágenes (por ejemplo, otro agente o un MCP de generación). Mientras tanto, sirve como guía de criterios de calidad.

**Relacionadas** (mismo repositorio, solo producen imágenes): `imagegen-frontend-web`, `imagegen-frontend-mobile`, `brandkit`.

**Cómo aplicarla en este portfolio:**
- Las imágenes generadas deben ser composiciones genéricas: nada de logos, marcas ni pantallas reales de clientes.
- Si se generan referencias visuales, usarlas como guía de composición y tipografía, y revisarlas con Ana antes de pasarlas a código.
- Mantener el hero limpio y legible en un portátil pequeño, y evitar el exceso de tarjetas y etiquetas.

---

## 5. playwright-cli (Microsoft Playwright): OMITIDA

- **Web:** https://playwright.dev/agent-cli/introduction (skills: https://playwright.dev/agent-cli/skills)
- **Estado:** OMITIDA por decisión de Ana (2026-10-19): no quiere instalar Node.js. No tener en cuenta en el trabajo del portfolio. Las capturas a distintos anchos no se pueden automatizar; revisar abriendo `index.html` en el navegador.
- **Fecha:** 2026-10-19

**Qué hace:** CLI para que un agente controle un navegador desde el terminal: abrir páginas, capturas, PDF, redimensionar, leer consola y red, grabar vídeo, etc. Útil para ver el portfolio a distintos anchos y verificar visualmente los cambios.

**Pasos de instalación:**
1. Instalar Node.js LTS desde https://nodejs.org (puede requerir permisos de IT).
2. `npm install -g @playwright/cli`
3. Skill para Claude Code: `playwright-cli install --skills` (copia a `.claude/skills/playwright-cli` del directorio actual) o `playwright-cli install --skills -g` (disponible en todos los proyectos).
4. Si hace falta navegador: `playwright-cli install-browser [browser]`. Con Chrome instalado puede no ser necesario.

Comandos útiles: `open <url>`, `resize <w> <h>`, `screenshot`, `console`, `--help [comando]`.

**Cómo aplicarla en este portfolio:**
- Cuando esté instalada: abrir `index.html` y capturar a 3 anchos (móvil ~390, tablet ~768, escritorio ~1440) tras cada cambio visual.
- Apoya a web-design-guidelines (revisión de código) y a taste-skill (que necesita Chrome/Chromium para sus comprobaciones).
- Para ejecutar comandos desde esta sesión, Ana puede usar el prefijo `! `.

---

## Plantilla

```
## N. nombre-skill (autor)

- **Comando indicado:** `...`
- **Repositorio / web:**
- **Estado:** registrada / instalada
- **Fecha:**

**Qué hace:**
**Cómo aplicarla en este portfolio:**
```
