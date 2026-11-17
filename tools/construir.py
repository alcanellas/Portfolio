#!/usr/bin/env python3
"""Construye las páginas de proyecto, las tarjetas de Inicio y los enlaces Anterior/Siguiente
a partir de las FICHAS de la carpeta fichas/.

Uso (desde la carpeta del portfolio):
    python3 tools/construir.py            # construye todo
    python3 tools/construir.py --solo-comprobar   # valida las fichas sin escribir nada

Qué hace:
  1. Lee fichas/orden.txt (orden de los proyectos en la web, de arriba abajo).
  2. Por cada proyecto que tenga ficha (fichas/<archivo>.txt) genera proyectos/<archivo>.html.
       tipo: confidencial -> estructura FIJA, siempre igual (portada con candado, Descripción,
                             En qué consistió, Herramientas y aviso de confidencialidad).
       tipo: abierto      -> estructura configurable con [seccion ...] (texto, lista, imagen, galería...).
  3. Reescribe las tarjetas de index.html y los enlaces Anterior/Siguiente de TODAS las páginas de proyecto.
  4. Escribe js/i18n-proyectos.js con las traducciones al español de los proyectos (no se edita a mano).
  5. Los proyectos de orden.txt SIN ficha (por ejemplo design-system-marca-blanca) son páginas hechas a mano:
     no se regeneran, pero sí se ordenan y se enlazan.

Formato de las fichas: ver fichas/_plantilla-confidencial.txt y fichas/_plantilla-abierto.txt.
"""
import html
import os
import re
import sys
import urllib.parse

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FICHAS = os.path.join(RAIZ, "fichas")
PROY = os.path.join(RAIZ, "proyectos")
INDEX = os.path.join(RAIZ, "index.html")
I18N_JS = os.path.join(RAIZ, "js", "i18n.js")
I18N_PROY = os.path.join(RAIZ, "js", "i18n-proyectos.js")
CORREO = "alcanellass@gmail.com"
SUFIJO_TITULO = " · Ana López Canellas"

AVISOS = []          # avisos no fatales
SOLO_COMPROBAR = "--solo-comprobar" in sys.argv


class FichaError(Exception):
    pass


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def escribir(ruta, texto):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)


# ----------------------------------------------------------------------------------------------
# Traducciones comunes (las del resto de la web; el español se lee de js/i18n.js)
# ----------------------------------------------------------------------------------------------
COMUN_EN = {
    "skip_to_content": "Skip to content", "main": "Main", "projects": "Projects",
    "about_me": "About me", "language": "Language", "dark_mode": "Dark mode", "date": "Date",
    "company": "Company", "description": "Description", "what_it_involved": "What it involved",
    "tools": "Tools", "back_to_projects": "Back to projects", "previous": "Previous", "next": "Next",
    "more_projects": "More projects", "back_to_top": "Back to top", "confidential_client": "Confidential client",
    "project_protected_by_a_confidentiality_agreement": "Project protected by a confidentiality agreement",
    "get_in_touch_if_you_would": "Get in touch if you would like to know more about it.", "email_me": "Email me",
    "previous_slide": "Previous slide", "next_slide": "Next slide",
}
ES_COMUN = {}


def cargar_es_comun():
    js = leer(I18N_JS)
    bloque = js[js.index("var ES = {"):js.index("// Textos que se usan desde JavaScript")]
    for k, v in re.findall(r'^\s*"([\w-]+)":\s*"((?:[^"\\]|\\.)*)"', bloque, re.M):
        ES_COMUN[k] = bytes(v, "utf-8").decode("unicode_escape").encode("latin-1", "ignore").decode("utf-8", "ignore") \
            if "\\" in v else v
    faltan = [k for k in COMUN_EN if k not in ES_COMUN]
    if faltan:
        raise FichaError("faltan en js/i18n.js las claves comunes: " + ", ".join(faltan))


# Logos conocidos de herramientas: nombre en minúsculas -> (archivo en assets/img, logo de un solo color)
LOGOS = {
    "figma": ("logo-figma.svg", False), "figma make": ("logo-figma.svg", False),
    "claude": ("logo-claude-code.svg", False), "claude code": ("logo-claude-code.svg", False), "jira": ("logo-jira.svg", False),
    "atlassian": ("logo-atlassian.svg", False), "voiceover (ios)": ("logo-apple.svg", True),
    "voiceover": ("logo-apple.svg", True), "apple": ("logo-apple.svg", True),
}

# ----------------------------------------------------------------------------------------------
# Lectura de fichas
# ----------------------------------------------------------------------------------------------


def parsear(texto, nombre):
    """Devuelve (campos, secciones). Cada sección = {'tipo', 'campos', 'items': [(nombre, campos)]}."""
    lineas = texto.split("\n")
    campos = {}
    secciones = []
    destino = campos
    i = 0

    def err(n, msg):
        raise FichaError(f"{nombre}, línea {n + 1}: {msg}")

    while i < len(lineas):
        linea = lineas[i]
        s = linea.strip()
        if not s or s.startswith("#"):
            i += 1
            continue
        m = re.match(r"^\[seccion\s+([\w-]+)\]$", s)
        if m:
            sec = {"tipo": m.group(1), "campos": {}, "items": []}
            secciones.append(sec)
            destino = sec["campos"]
            i += 1
            continue
        m = re.match(r"^\[\[([\w-]+)\]\]$", s)
        if m:
            if not secciones:
                err(i, "un [[elemento]] debe ir dentro de una [seccion ...]")
            item = {}
            secciones[-1]["items"].append((m.group(1), item))
            destino = item
            i += 1
            continue
        m = re.match(r"^([\w-]+):\s*(.*)$", s)
        if not m:
            err(i, f"no entiendo esta línea: {s[:60]!r}. Debe ser 'clave: valor', '[seccion tipo]' o '[[elemento]]'")
        clave, valor = m.group(1), m.group(2)
        if valor == "|":                                   # texto de varias líneas
            bloque = []
            i += 1
            while i < len(lineas) and (not lineas[i].strip() or lineas[i][:1] in (" ", "\t")):
                bloque.append(lineas[i])
                i += 1
            while bloque and not bloque[-1].strip():
                bloque.pop()
            indent = min((len(l) - len(l.lstrip()) for l in bloque if l.strip()), default=0)
            destino[clave] = "\n".join(l[indent:] if l.strip() else "" for l in bloque)
            continue
        if valor == "":                                    # lista con "- elemento"
            items = []
            i += 1
            while i < len(lineas) and (not lineas[i].strip() or lineas[i].lstrip().startswith("- ") or lineas[i].lstrip().startswith("#")):
                t = lineas[i].strip()
                if t.startswith("- "):
                    items.append(t[2:].strip())
                i += 1
            destino[clave] = items
            continue
        destino[clave] = re.sub(r"\s{2,}#.*$", "", valor).strip()   # comentario al final de la línea
        i += 1
    return campos, secciones


def req(campos, clave, nombre):
    v = campos.get(clave)
    if v in (None, "", []):
        raise FichaError(f"{nombre}: falta el campo '{clave}'")
    return v


def bi(campos, base, nombre, obligatorio=True):
    """Devuelve (inglés, español) de los campos base_en y base_es."""
    en = campos.get(base + "_en")
    es = campos.get(base + "_es")
    if en in (None, "", []):
        if obligatorio:
            raise FichaError(f"{nombre}: falta '{base}_en'")
        return None, None
    if es in (None, "", []):
        AVISOS.append(f"{nombre}: falta '{base}_es'; en español se verá el texto en inglés")
        es = en
    if isinstance(en, list) and isinstance(es, list) and len(en) != len(es):
        raise FichaError(f"{nombre}: '{base}_en' tiene {len(en)} elementos y '{base}_es' tiene {len(es)}; deben coincidir")
    return en, es


# ----------------------------------------------------------------------------------------------
# Piezas de HTML
# ----------------------------------------------------------------------------------------------
LOCK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true"><rect x="4" y="11" width="16" height="10" rx="3"/>'
        '<path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>')
ARROW_L = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
           'stroke-linejoin="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>')
ARROW_R = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" '
           'stroke-linejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>')
THEME_BTN = ('<button class="theme-toggle" type="button" aria-pressed="false" aria-label="Dark mode" data-i18n-aria-label="dark_mode">\n'
             '          <svg class="i-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>\n'
             '          <svg class="i-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>\n'
             '        </button>')


class Proyecto:
    """Todo lo necesario de un proyecto: ficha leída + textos registrados para el idioma."""

    def __init__(self, ruta):
        self.ruta = ruta
        self.nombre = os.path.basename(ruta)
        campos, secciones = parsear(leer(ruta), self.nombre)
        self.campos, self.secciones = campos, secciones
        self.slug = req(campos, "archivo", self.nombre)
        if not re.match(r"^[a-z0-9][a-z0-9-]*$", self.slug):
            raise FichaError(f"{self.nombre}: 'archivo' solo puede llevar minúsculas, números y guiones (ej. retail-ecommerce)")
        if self.slug + ".txt" != self.nombre:
            raise FichaError(f"{self.nombre}: el nombre del archivo debe coincidir con 'archivo' ({self.slug}.txt)")
        self.tipo = req(campos, "tipo", self.nombre)
        if self.tipo not in ("confidencial", "abierto"):
            raise FichaError(f"{self.nombre}: 'tipo' debe ser 'confidencial' o 'abierto'")
        self.anio = req(campos, "anio", self.nombre)
        self.empresa = campos.get("empresa", "Accenture Spain")
        self.titulo = bi(campos, "titulo", self.nombre)
        et_en, et_es = bi(campos, "etiquetas", self.nombre)
        lista_en = [x.strip() for x in et_en.split(",") if x.strip()]
        lista_es = [x.strip() for x in et_es.split(",") if x.strip()]
        if len(lista_en) != len(lista_es):
            raise FichaError(f"{self.nombre}: 'etiquetas_en' tiene {len(lista_en)} etiquetas y 'etiquetas_es' {len(lista_es)}; deben coincidir")
        self.etiquetas = (lista_en, lista_es)
        # etiquetas de la tarjeta de Inicio (opcional): si no se indican, son las mismas que en la página
        tc_en, tc_es = bi(campos, "etiquetas_tarjeta", self.nombre, obligatorio=False)
        if tc_en:
            ce = [x.strip() for x in tc_en.split(",") if x.strip()]
            cs = [x.strip() for x in tc_es.split(",") if x.strip()]
            if len(ce) != len(cs):
                raise FichaError(f"{self.nombre}: 'etiquetas_tarjeta_en' y 'etiquetas_tarjeta_es' deben tener las mismas etiquetas")
            self.etiquetas_tarjeta = (ce, cs)
        else:
            self.etiquetas_tarjeta = self.etiquetas
        self.reg = {}            # clave -> español
        self.pref = "p_" + self.slug.replace("-", "_") + "_"
        if self.tipo == "confidencial" and secciones:
            raise FichaError(f"{self.nombre}: los proyectos CONFIDENCIALES tienen siempre la misma estructura y no admiten "
                             f"[seccion ...]. Usa 'descripcion', 'hizo' y 'herramientas'; o cambia 'tipo: abierto'.")
        self.validar_campos()

    CAMPOS_CONF = {"tipo", "archivo", "anio", "empresa", "titulo_en", "titulo_es", "etiquetas_en", "etiquetas_es", "etiquetas_tarjeta_en", "etiquetas_tarjeta_es", "sector_en", "sector_es",
                   "descripcion_en", "descripcion_es", "meta_en", "meta_es", "hizo_en", "hizo_es", "herramientas",
                   "portada_alt_en", "portada_alt_es"}
    CAMPOS_ABIERTO = (CAMPOS_CONF - {"descripcion_en", "descripcion_es", "hizo_en", "hizo_es", "herramientas"}) | {
        "portada", "portada_etiqueta_en", "portada_etiqueta_es", "meta_en", "meta_es"}

    def validar_campos(self):
        permitidos = self.CAMPOS_CONF if self.tipo == "confidencial" else self.CAMPOS_ABIERTO
        for c in self.campos:
            if c not in permitidos:
                AVISOS.append(f"{self.nombre}: el campo '{c}' no se usa en proyectos '{self.tipo}' (se ignora). "
                              f"Comprueba que no esté mal escrito")

    # --- registro de textos traducibles ---------------------------------------------------------
    def clave(self, nombre):
        return self.pref + nombre

    def T(self, nombre, en, es):
        """Atributo data-i18n para un texto; registra la traducción si es distinta."""
        if en == es:
            return ""
        k = self.clave(nombre)
        self.reg[k] = es
        return f' data-i18n="{k}"'

    def TA(self, attr, nombre, en, es):
        if en == es:
            return ""
        k = self.clave(nombre)
        self.reg[k] = es
        return f' data-i18n-{attr}="{k}"'


def esc(t):
    return html.escape(t, quote=False)


def esca(t):
    return html.escape(t, quote=True)


def parrafos(t):
    return [re.sub(r"\s*\n\s*", " ", p).strip() for p in re.split(r"\n\s*\n", t.strip()) if p.strip()]


def comun_attr(clave_, attr=None):
    ES_COMUN_USADAS[clave_] = ES_COMUN[clave_]
    return f' data-i18n-{attr}="{clave_}"' if attr else f' data-i18n="{clave_}"'


ES_COMUN_USADAS = {}

# ----------------------------------------------------------------------------------------------
# Herramientas
# ----------------------------------------------------------------------------------------------


def lista_herramientas(texto, pre):
    items = []
    for t in [x.strip() for x in texto.split(",") if x.strip()]:
        partes = [p.strip() for p in t.split("|")]
        nombre = partes[0]
        logo, mono = LOGOS.get(nombre.lower(), (None, False))
        if len(partes) > 1:
            logo = partes[1]
            mono = len(partes) > 2 and partes[2] == "mono"
        if logo and not os.path.exists(os.path.join(RAIZ, "assets", "img", logo)):
            AVISOS.append(f"herramienta '{nombre}': no existe assets/img/{logo}; se mostrará sin logo")
            logo = None
        if logo:
            cls = ' class="logo-mono"' if mono else ""
            items.append(f'<li><img{cls} src="{pre}assets/img/{logo}" alt="" width="24" height="24"><span>{esc(nombre)}</span></li>')
        else:
            items.append(f"<li><span>{esc(nombre)}</span></li>")
    return items


def bloque_herramientas(p, pre, titulo=None, herramientas_txt=""):
    t_en, t_es = titulo if titulo else ("Tools", ES_COMUN["tools"])
    if titulo:
        h2 = f'<h2 class="h4"{p.T("tools_title", t_en, t_es)}>{esc(t_en)}</h2>'
    else:
        h2 = f'<h2 class="h4"{comun_attr("tools")}>Tools</h2>'
    lis = "\n".join("            " + li for li in lista_herramientas(herramientas_txt, pre))
    return ('        <section class="tools">\n'
            f"          {h2}\n"
            '          <ul class="tools-list" role="list">\n'
            f"{lis}\n"
            "          </ul>\n"
            "        </section>")


# ----------------------------------------------------------------------------------------------
# Secciones de los proyectos ABIERTOS (y piezas de los confidenciales)
# ----------------------------------------------------------------------------------------------

def titulo_seccion(p, n, campos, pre_id):
    en, es = bi(campos, "titulo", f"{p.nombre} sección {n}", obligatorio=False)
    if en is None:
        return "", None
    return f'<h2 class="h4" id="{pre_id}"{p.T(f"s{n}_titulo", en, es)}>{esc(en)}</h2>', (en, es)


def sec_texto(p, n, sec, pre):
    c = sec["campos"]
    h2, _ = titulo_seccion(p, n, c, f"s{n}")
    en, es = bi(c, "texto", f"{p.nombre} sección {n} (texto)")
    pe, ps = parrafos(en), parrafos(es)
    if len(pe) != len(ps):
        raise FichaError(f"{p.nombre} sección {n}: 'texto_en' tiene {len(pe)} párrafos y 'texto_es' {len(ps)}")
    ps_html = "\n".join(f'          <p class="summary"{p.T(f"s{n}_p{i + 1}", a, b)}>{esc(a)}</p>' for i, (a, b) in enumerate(zip(pe, ps)))
    return ("        <section>\n" + (f"          {h2}\n" if h2 else "") + ps_html + "\n        </section>")


def sec_lista(p, n, sec, pre):
    c = sec["campos"]
    h2, _ = titulo_seccion(p, n, c, f"s{n}")
    en, es = bi(c, "items", f"{p.nombre} sección {n} (lista)")
    lis = "\n".join(f'            <li{p.T(f"s{n}_i{i + 1}", a, b)}>{esc(a)}</li>' for i, (a, b) in enumerate(zip(en, es)))
    return ("        <section>\n" + (f"          {h2}\n" if h2 else "") +
            '          <ul class="tasks">\n' + lis + "\n          </ul>\n        </section>")


def sec_herramientas(p, n, sec, pre):
    c = sec["campos"]
    t = bi(c, "titulo", f"{p.nombre} sección {n}", obligatorio=False)
    return bloque_herramientas(p, pre, titulo=t if t[0] else None, herramientas_txt=req(c, "herramientas", f"{p.nombre} sección {n} (herramientas)"))


def figura(p, pre, n, i, campos, nombre_sec, clase="", lazy=True):
    arch = req(campos, "archivo", f"{p.nombre} {nombre_sec}")
    if not os.path.exists(os.path.join(RAIZ, "assets", "img", arch)):
        AVISOS.append(f"{p.nombre} {nombre_sec}: no existe assets/img/{arch} (la imagen no se verá hasta que la subas)")
    ae, as_ = bi(campos, "alt", f"{p.nombre} {nombre_sec}")
    pe, ps = bi(campos, "pie", f"{p.nombre} {nombre_sec}", obligatorio=False)
    cap = f"\n            <figcaption{p.T(f's{n}_f{i}_pie', pe, ps)}>{esc(pe)}</figcaption>" if pe else ""
    loading = ' loading="lazy"' if lazy else ""
    return (f'          <figure{(" class=" + chr(34) + clase + chr(34)) if clase else ""}>\n'
            f'            <img src="{pre}assets/img/{esca(arch)}" alt="{esca(ae)}"{p.TA("alt", f"s{n}_f{i}_alt", ae, as_)}{loading}>{cap}\n'
            "          </figure>")


def sec_imagen(p, n, sec, pre):
    c = sec["campos"]
    h2, _ = titulo_seccion(p, n, c, f"s{n}")
    ajuste = c.get("ajuste", "entera")
    if ajuste not in ("entera", "recortada"):
        raise FichaError(f"{p.nombre} sección {n}: 'ajuste' debe ser 'entera' o 'recortada'")
    clase = "figure-full" if ajuste == "entera" else "figure-crop"
    return ("        <section>\n" + (f"          {h2}\n" if h2 else "") +
            figura(p, pre, n, 1, c, f"sección {n} (imagen)", clase) + "\n        </section>")


def sec_galeria(p, n, sec, pre):
    c = sec["campos"]
    h2, _ = titulo_seccion(p, n, c, f"s{n}")
    cols = c.get("columnas", "2")
    if cols not in ("2", "3"):
        raise FichaError(f"{p.nombre} sección {n}: 'columnas' debe ser 2 o 3")
    figs = [figura(p, pre, n, i + 1, it, f"sección {n} imagen {i + 1}") for i, (nm, it) in enumerate(sec["items"]) if nm == "imagen"]
    if not figs:
        raise FichaError(f"{p.nombre} sección {n} (galeria): añade al menos un [[imagen]]")
    return ("        <section>\n" + (f"          {h2}\n" if h2 else "") +
            f'          <div class="block-grid cols-{cols}">\n' + "\n".join(figs) + "\n          </div>\n        </section>")


def sec_carrusel(p, n, sec, pre):
    c = sec["campos"]
    h2, t = titulo_seccion(p, n, c, f"s{n}")
    items = [it for nm, it in sec["items"] if nm == "diapositiva"]
    if not items:
        raise FichaError(f"{p.nombre} sección {n} (carrusel): añade al menos una [[diapositiva]]")
    lab_en = t[0] if t else "Slides"
    lab_es = t[1] if t else "Diapositivas"
    total = len(items)
    lis = []
    for i, it in enumerate(items):
        ar = f"{i + 1} of {total}"
        ae = f"{i + 1} de {total}"
        k = f"{i + 1}_of_{total}"
        p.reg[k] = ae
        fig = figura(p, pre, n, i + 1, it, f"sección {n} diapositiva {i + 1}", "figure-slide")
        lis.append(f'            <li class="carousel-slide" role="group" aria-roledescription="slide" aria-label="{ar}" data-i18n-aria-label="{k}">\n'
                   + fig.replace("          <figure", "              <figure").replace("            <img", "                <img").replace("            <figcaption", "                <figcaption").replace("          </figure>", "              </figure>")
                   + "\n            </li>")
    p.reg["carousel"] = "carrusel"
    p.reg["slide"] = "diapositiva"
    p.reg["slides"] = "Diapositivas"
    return ("        <section>\n" + (f"          {h2}\n" if h2 else "") +
            f'          <div class="carousel" role="region" aria-roledescription="carousel" data-i18n-aria-roledescription="carousel" aria-label="{esca(lab_en)}"{p.TA("aria-label", f"s{n}_label", lab_en, lab_es)}>\n'
            f'            <button class="carousel-arrow carousel-prev" type="button" aria-label="Previous slide" hidden{comun_attr("previous_slide", "aria-label")}>{ARROW_L}</button>\n'
            f'            <ul class="carousel-track" role="list" tabindex="0" aria-label="Slides" data-i18n-aria-label="slides">\n'
            + "\n".join(lis) + "\n            </ul>\n"
            f'            <button class="carousel-arrow carousel-next" type="button" aria-label="Next slide" hidden{comun_attr("next_slide", "aria-label")}>{ARROW_R}</button>\n'
            '            <div class="carousel-dots" hidden></div>\n'
            '            <p class="carousel-status sr-only" aria-live="polite"></p>\n'
            "          </div>\n        </section>").replace('aria-roledescription="slide" aria-label', 'aria-roledescription="slide" data-i18n-aria-roledescription="slide" aria-label')


def sec_tarjetas(p, n, sec, pre):
    c = sec["campos"]
    h2, _ = titulo_seccion(p, n, c, f"s{n}")
    ie, is_ = bi(c, "intro", f"{p.nombre} sección {n}", obligatorio=False)
    intro = f'          <p class="gallery-intro"{p.T(f"s{n}_intro", ie, is_)}>{esc(ie)}</p>\n' if ie else ""
    cards = []
    items = [it for nm, it in sec["items"] if nm == "tarjeta"]
    if not items:
        raise FichaError(f"{p.nombre} sección {n} (tarjetas): añade al menos una [[tarjeta]]")
    for i, it in enumerate(items):
        me, ms = bi(it, "etiqueta", f"{p.nombre} sección {n} tarjeta {i + 1}", obligatorio=False)
        te, ts = bi(it, "titulo", f"{p.nombre} sección {n} tarjeta {i + 1}")
        xe, xs = bi(it, "texto", f"{p.nombre} sección {n} tarjeta {i + 1}")
        meta = f'<p class="card-meta"{p.T(f"s{n}_c{i + 1}_etiqueta", me, ms)}>{esc(me)}</p>' if me else ""
        cards.append(f'            <li class="file-card">{meta}<h3{p.T(f"s{n}_c{i + 1}_titulo", te, ts)}>{esc(te)}</h3>'
                     f'<p{p.T(f"s{n}_c{i + 1}_texto", xe, xs)}>{esc(xe)}</p></li>')
    return ("        <section>\n" + (f"          {h2}\n" if h2 else "") + intro +
            '          <ul class="file-grid" role="list">\n' + "\n".join(cards) + "\n          </ul>\n        </section>")


def sec_texto_imagen(p, n, sec, pre):
    c = sec["campos"]
    h2, _ = titulo_seccion(p, n, c, f"s{n}")
    en, es = bi(c, "texto", f"{p.nombre} sección {n} (texto-imagen)")
    pe, ps = parrafos(en), parrafos(es)
    if len(pe) != len(ps):
        raise FichaError(f"{p.nombre} sección {n}: 'texto_en' y 'texto_es' deben tener los mismos párrafos")
    lado = c.get("lado", "derecha")
    if lado not in ("derecha", "izquierda"):
        raise FichaError(f"{p.nombre} sección {n}: 'lado' debe ser 'derecha' o 'izquierda'")
    ps_html = "\n".join(f'            <p{p.T(f"s{n}_p{i + 1}", a, b)}>{esc(a)}</p>' for i, (a, b) in enumerate(zip(pe, ps)))
    arch = req(c, "archivo", f"{p.nombre} sección {n} (texto-imagen)")
    if not os.path.exists(os.path.join(RAIZ, "assets", "img", arch)):
        AVISOS.append(f"{p.nombre} sección {n}: no existe assets/img/{arch} (se verá la portada de respaldo)")
    ae, as_ = bi(c, "alt", f"{p.nombre} sección {n} (texto-imagen)")
    cls = "workshops" + (" workshops-left" if lado == "izquierda" else "")
    return ("        <section>\n" + (f"          {h2}\n" if h2 else "") +
            f'          <div class="{cls}">\n'
            '            <div class="workshops-text">\n' + ps_html + "\n            </div>\n"
            '            <figure class="workshops-figure">\n'
            f'              <div class="card-cover cover-confidential"><img src="{pre}assets/img/{esca(arch)}" alt="{esca(ae)}"{p.TA("alt", f"s{n}_alt", ae, as_)} loading="lazy" width="1200" height="750"></div>\n'
            "            </figure>\n          </div>\n        </section>")


def sec_cita(p, n, sec, pre):
    c = sec["campos"]
    en, es = bi(c, "texto", f"{p.nombre} sección {n} (cita)")
    ae, as_ = bi(c, "autor", f"{p.nombre} sección {n} (cita)", obligatorio=False)
    autor = f'\n            <figcaption{p.T(f"s{n}_autor", ae, as_)}>{esc(ae)}</figcaption>' if ae else ""
    return ('        <section>\n          <figure class="quote">\n'
            f'            <blockquote><p{p.T(f"s{n}_texto", en, es)}>{esc(en)}</p></blockquote>{autor}\n'
            "          </figure>\n        </section>")


def sec_datos(p, n, sec, pre):
    c = sec["campos"]
    h2, _ = titulo_seccion(p, n, c, f"s{n}")
    items = [it for nm, it in sec["items"] if nm == "dato"]
    if not items:
        raise FichaError(f"{p.nombre} sección {n} (datos): añade al menos un [[dato]]")
    li = []
    for i, it in enumerate(items):
        v = req(it, "valor", f"{p.nombre} sección {n} dato {i + 1}")
        le, ls = bi(it, "etiqueta", f"{p.nombre} sección {n} dato {i + 1}")
        li.append(f'            <li><span class="stat-value">{esc(v)}</span><span class="stat-label"{p.T(f"s{n}_d{i + 1}", le, ls)}>{esc(le)}</span></li>')
    return ("        <section>\n" + (f"          {h2}\n" if h2 else "") +
            '          <ul class="stats" role="list">\n' + "\n".join(li) + "\n          </ul>\n        </section>")


def sec_enlace(p, n, sec, pre):
    c = sec["campos"]
    en, es = bi(c, "texto", f"{p.nombre} sección {n} (enlace)")
    url = req(c, "url", f"{p.nombre} sección {n} (enlace)")
    if not re.match(r"^https?://", url):
        raise FichaError(f"{p.nombre} sección {n}: 'url' debe empezar por http:// o https://")
    p.reg["opens_in_a_new_tab"] = "(se abre en una pestaña nueva)"
    return ('        <section>\n'
            f'          <a class="link-btn" href="{esca(url)}" target="_blank" rel="noopener"><span{p.T(f"s{n}_texto", en, es)}>{esc(en)}</span> <span aria-hidden="true">↗</span>'
            '<span class="sr-only" data-i18n="opens_in_a_new_tab"> (opens in a new tab)</span></a>\n'
            "        </section>")


SECCIONES = {
    "texto": (sec_texto, "mitad"), "lista": (sec_lista, "mitad"), "herramientas": (sec_herramientas, "fila"),
    "imagen": (sec_imagen, None), "galeria": (sec_galeria, None), "carrusel": (sec_carrusel, None),
    "tarjetas": (sec_tarjetas, None), "texto-imagen": (sec_texto_imagen, None), "cita": (sec_cita, None),
    "datos": (sec_datos, None), "enlace": (sec_enlace, None),
}


def cuerpo_abierto(p, pre):
    """Agrupa las secciones: las 'mitad' consecutivas y las herramientas van en la rejilla de 2 columnas."""
    trozos = []          # (tipo, [html])
    for n, sec in enumerate(p.secciones, 1):
        t = sec["tipo"]
        if t not in SECCIONES:
            raise FichaError(f"{p.nombre}: tipo de sección desconocido '[seccion {t}]'. Disponibles: " + ", ".join(sorted(SECCIONES)))
        fn, modo = SECCIONES[t]
        ancho = sec["campos"].get("ancho", "completo")
        if ancho not in ("completo", "mitad"):
            raise FichaError(f"{p.nombre} sección {n}: 'ancho' debe ser 'completo' o 'mitad'")
        enfila = (t == "herramientas") or (t in ("texto", "lista") and ancho == "mitad")
        htmln = fn(p, n, sec, pre)
        if enfila and trozos and trozos[-1][0] == "fila":
            trozos[-1][1].append(htmln)
        elif enfila:
            trozos.append(("fila", [htmln]))
        else:
            trozos.append(("bloque", [htmln]))
    salida = []
    for i, (tipo, partes) in enumerate(trozos):
        extra = "" if i == 0 else " project-gap"
        if tipo == "fila":
            salida.append(f'      <div class="project-body{extra}">\n' + "\n".join(partes) + "\n      </div>")
        else:
            salida.append(f'      <div class="project-block{extra}">\n' + "\n".join(partes) + "\n      </div>")
    return "\n\n".join(salida)


def cuerpo_confidencial(p, pre):
    c = p.campos
    de, ds = bi(c, "descripcion", p.nombre)
    pe, ps = parrafos(de), parrafos(ds)
    if len(pe) != len(ps):
        raise FichaError(f"{p.nombre}: 'descripcion_en' tiene {len(pe)} párrafos y 'descripcion_es' {len(ps)}; deben coincidir")
    he, hs = bi(c, "hizo", p.nombre)
    # el texto de la descripción se registra con la misma clave que usa la meta description
    p.meta_clave = None
    if len(pe) >= 1 and pe[0] != ps[0]:
        p.meta_clave = p.clave("desc_1")
    pars = "\n".join(f'          <p class="summary"{p.T(f"desc_{i + 1}", a, b)}>{esc(a)}</p>' for i, (a, b) in enumerate(zip(pe, ps)))
    lis = "\n".join(f'            <li{p.T(f"hizo_{i + 1}", a, b)}>{esc(a)}</li>' for i, (a, b) in enumerate(zip(he, hs)))
    return ('      <div class="project-body">\n'
            "        <section>\n"
            f'          <h2 class="h4"{comun_attr("description")}>Description</h2>\n'
            f"{pars}\n"
            "        </section>\n"
            "        <section>\n"
            f'          <h2 class="h4"{comun_attr("what_it_involved")}>What it involved</h2>\n'
            '          <ul class="tasks">\n'
            f"{lis}\n"
            "          </ul>\n"
            "        </section>\n"
            + bloque_herramientas(p, pre, None, req(c, "herramientas", p.nombre)) + "\n"
            "      </div>")


def aviso_nda(p):
    asunto_en = urllib.parse.quote(p.titulo[0])
    asunto_es = urllib.parse.quote(p.titulo[1])
    href_en = f"mailto:{CORREO}?subject={asunto_en}"
    href_es = f"mailto:{CORREO}?subject={asunto_es}"
    attr = ""
    if href_en != href_es:
        p.reg[p.clave("mail")] = href_es
        attr = f' data-i18n-href="{p.clave("mail")}"'
    return ('      <section class="nda-note" aria-labelledby="nda-t">\n'
            f'        <span class="nda-note-icon" aria-hidden="true">{LOCK.replace(" aria-hidden=" + chr(34) + "true" + chr(34), "")}</span>\n'
            '        <div class="nda-note-body">\n'
            f'          <h2 id="nda-t" class="nda-note-title"{comun_attr("project_protected_by_a_confidentiality_agreement")}>Project protected by a confidentiality agreement</h2>\n'
            f'          <p{comun_attr("get_in_touch_if_you_would")}>Get in touch if you would like to know more about it.</p>\n'
            "        </div>\n"
            f'        <a class="nda-btn" href="{href_en}"{attr}{comun_attr("email_me")}>Email me</a>\n'
            "      </section>")


def portada(p, pre):
    """Portada de la página. Confidencial: con candado y etiqueta. Abierto: sin candado."""
    c = p.campos
    arch = c.get("portada", p.slug + ".jpg") if p.tipo == "abierto" else p.slug + ".jpg"
    alt = bi(c, "portada_alt", p.nombre, obligatorio=False)
    if alt[0] is None:
        AVISOS.append(f"{p.nombre}: falta 'portada_alt_en' (texto alternativo de la portada); descríbela para accesibilidad")
        alt = (f"Cover image of the project {p.titulo[0]}", f"Imagen de portada del proyecto {p.titulo[1]}")
    alt_attr = f'alt="{esca(alt[0])}"{p.TA("alt", "portada_alt", alt[0], alt[1])}'
    if p.tipo == "confidencial":
        return (f'      <div class="cover cover-confidential cover-keep-lock"><img src="{pre}assets/img/{arch}" {alt_attr} loading="eager" width="1200" height="750">'
                f'<span class="lock">{LOCK}</span><span class="conf-label"{comun_attr("confidential_client")}>Confidential client</span></div>')
    le, ls = bi(c, "portada_etiqueta", p.nombre, obligatorio=False)
    lab = f'<span class="conf-label"{p.T("portada_etiqueta", le, ls)}>{esc(le)}</span>' if le else ""
    return (f'      <div class="cover cover-confidential"><img src="{pre}assets/img/{arch}" {alt_attr} loading="eager" width="1200" height="750">{lab}</div>')


def tarjeta(p):
    """Tarjeta de la portada de Inicio."""
    c = p.campos
    arch = c.get("portada", p.slug + ".jpg") if p.tipo == "abierto" else p.slug + ".jpg"
    sen, ses = bi(c, "sector", p.nombre, obligatorio=False)
    sector_pill = f'<span{p.T("card_sector", sen, ses)}>{esc(sen)}</span> <span aria-hidden="true">•</span> ' if sen else ""
    if p.tipo == "confidencial":
        cover = (f'<div class="card-cover cover-confidential cover-keep-lock"><img src="assets/img/{arch}" alt="" loading="lazy" width="1200" height="750">'
                 f'<span class="lock">{LOCK}</span><span class="conf-label">{sector_pill}<span{comun_attr("confidential_client")}>Confidential client</span></span></div>')
    else:
        le, ls = bi(c, "portada_etiqueta", p.nombre, obligatorio=False)
        lab = f'<span class="conf-label"{p.T("portada_etiqueta", le, ls)}>{esc(le)}</span>' if le else ""
        cover = f'<div class="card-cover cover-confidential"><img src="assets/img/{arch}" alt="" loading="lazy" width="1200" height="750">{lab}</div>'
    tags = "".join(f'<li{p.T(f"card_tag_{i + 1}", a, b)}>{esc(a)}</li>' for i, (a, b) in enumerate(zip(*p.etiquetas_tarjeta)))
    filtro = f' data-company="{esca(p.empresa)}" data-year="{esca(p.anio)}"' + (f' data-sector="{esca(sen)}" data-sector-es="{esca(ses)}"' if sen else "")
    # El tipo de cliente va encima del nombre; si el título empieza por "Sector · ", el nombre queda sin ese prefijo
    h3_en, h3_es = p.titulo
    if sen and " · " in h3_en and " · " in h3_es:
        h3_en, h3_es = h3_en.split(" · ", 1)[1], h3_es.split(" · ", 1)[1]
    h3_attr = p.T("card_titulo", h3_en, h3_es) if (h3_en, h3_es) != tuple(p.titulo) else p.T("titulo", *p.titulo)
    return (f'      <a class="card" href="proyectos/{p.slug}.html"{filtro}>\n'
            '        <div class="card-body">\n'
            f'          <p class="card-meta"><time datetime="{esca(p.anio)}">{esc(p.anio)}</time><span class="card-company">{esc(p.empresa)}</span></p>\n'
            f'          <h3{h3_attr}>{esc(h3_en)}</h3>\n'
            f'          <ul class="tags" role="list">{tags}</ul>\n'
            "        </div>\n"
            f"        {cover}\n"
            "      </a>\n")


def separar_descripcion(cuerpo):
    """Saca la sección Description del cuerpo para colocarla antes de la portada. Devuelve (intro, resto)."""
    m = re.match(r'      <div class="project-body">\n        <section>\n(.*?)        </section>\n', cuerpo, re.S)
    if not m:
        return "", cuerpo
    intro = '      <section class="project-intro">\n' + m.group(1) + '      </section>\n\n'
    return intro, '      <div class="project-body">\n' + cuerpo[m.end():]


def pagina(p, anterior, siguiente):
    pre = "../"
    c = p.campos
    titulo_en, titulo_es = p.titulo
    # meta description: la de la ficha o el primer párrafo de la descripción
    if p.tipo == "confidencial":
        intro, cuerpo = separar_descripcion(cuerpo_confidencial(p, pre))
        den, des = bi(c, "descripcion", p.nombre)
        meta_en_def = parrafos(den)[0]
        meta_es_def = parrafos(des)[0]
    else:
        intro, cuerpo = "", cuerpo_abierto(p, pre)
        meta_en_def = f"{titulo_en}, a project by Ana López Canellas."
        meta_es_def = f"{titulo_es}, un proyecto de Ana López Canellas."
    men, mes = bi(c, "meta", p.nombre, obligatorio=False)
    if men is None:
        men, mes = meta_en_def, meta_es_def
    meta_attr = p.TA("content", "meta", men, mes)
    nda = ("\n\n" + aviso_nda(p)) if p.tipo == "confidencial" else ""
    meta_item = (f'<p class="meta"><span class="meta-item"><span{comun_attr("date")}>Date</span> <time datetime="{esca(p.anio)}">{esc(p.anio)}</time></span>'
                 f'<span class="meta-item"><span{comun_attr("company")}>Company</span> {esc(p.empresa)}</span></p>')
    tags = "".join(f'<li{p.T(f"tag_{i + 1}", a, b)}>{esc(a)}</li>' for i, (a, b) in enumerate(zip(*p.etiquetas)))
    # Anterior / Siguiente
    def enlace(dest, lado):
        t = f'<span{dest["attr"]}>{esc(dest["en"])}</span>' if dest["attr"] else esc(dest["en"])
        if lado == "ant":
            lab = f'<span><span aria-hidden="true">← </span><span{comun_attr("previous")}>Previous</span></span>'
        else:
            lab = f'<span><span{comun_attr("next")}>Next</span><span aria-hidden="true"> →</span></span>'
        return f'        <a href="{dest["slug"]}.html">{lab}{t}</a>'
    pager = ('      <nav class="pager" aria-label="More projects"' + comun_attr("more_projects", "aria-label") + ">\n"
             + enlace(anterior, "ant") + "\n" + enlace(siguiente, "sig") + "\n      </nav>")
    titulo_pagina = titulo_en + SUFIJO_TITULO
    titulo_pagina_es = titulo_es + SUFIJO_TITULO
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">
  <title{p.T("titulo_pagina", titulo_pagina, titulo_pagina_es)}>{esc(titulo_pagina)}</title>
  <meta name="description" content="{esca(men)}"{meta_attr}>
  <link rel="icon" type="image/svg+xml" href="../assets/img/logo-color.svg">
  <link rel="preload" href="../assets/fonts/raleway-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="../assets/fonts/inter-latin.woff2" as="font" type="font/woff2" crossorigin>
  <script>(function(){{try{{var t=localStorage.getItem('theme');if(t==='light'||t==='dark')document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}}})()</script>
  <link rel="stylesheet" href="../css/styles.css">
</head>
<body>
  <a class="skip" href="#main"{comun_attr("skip_to_content")}>Skip to content</a>

  <header class="header">
    <nav class="nav" aria-label="Main"{comun_attr("main", "aria-label")}>
      <a class="icon-link nav-home" href="../index.html#inicio"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9a1 1 0 0 0 1 1H10v-5h4v5h3.5a1 1 0 0 0 1-1v-9"/></svg><span class="sr-only" data-i18n="home">Home</span></a>
      <ul class="menu" role="list">
        <li class="menu-home"><a href="../index.html#inicio"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9a1 1 0 0 0 1 1H10v-5h4v5h3.5a1 1 0 0 0 1-1v-9"/></svg><span class="sr-only" data-i18n="home">Home</span></a></li>
        <li><a href="../index.html#trabajo" aria-current="page"{comun_attr("projects")}>Projects</a></li>
        <li><a href="../sobre-mi.html"{comun_attr("about_me")}>About me</a></li>
        <li class="menu-links"><button type="button" class="menu-links-btn" aria-expanded="false" aria-controls="header-tools"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.07 0l3-3a5 5 0 0 0-7.07-7.07l-1.5 1.5"/><path d="M14 11a5 5 0 0 0-7.07 0l-3 3a5 5 0 0 0 7.07 7.07l1.5-1.5"/></svg><span class="sr-only">Links</span></button></li>
      </ul>
      <div class="header-tools" id="header-tools">
        <a class="icon-link" href="https://www.linkedin.com/in/ana-l%C3%B3pez-canellas-795887292/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.75h4V21H3zM9.5 9.75h3.8v1.6h.05c.55-1 1.9-1.95 3.9-1.95 4.1 0 4.75 2.6 4.75 6V21h-4v-4.9c0-1.2 0-2.7-1.7-2.7s-1.95 1.3-1.95 2.6V21h-4z"/></svg><span class="sr-only">LinkedIn<span data-i18n="opens_in_a_new_tab"> (opens in a new tab)</span></span></a>
        <a class="icon-link" href="mailto:alcanellass@gmail.com"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 8 8 6 8-6"/></svg><span class="sr-only" data-i18n="email_me">Email me</span></a>
        {THEME_BTN}
        <div class="lang-switch" role="group" aria-label="Language"{comun_attr("language", "aria-label")}>
          <button type="button" class="lang-btn" data-lang="en" lang="en" aria-pressed="true" aria-label="English">EN</button>
          <button type="button" class="lang-btn" data-lang="es" lang="es" aria-pressed="false" aria-label="Español">ES</button>
        </div>
      </div>
    </nav>
  </header>

  <main id="main" tabindex="-1">
    <article class="project">
      <a class="back" href="../index.html#trabajo"><span aria-hidden="true">←</span> <span{comun_attr("back_to_projects")}>Back to projects</span></a>
      <header class="project-head">
        <h1{p.T("titulo", titulo_en, titulo_es)}>{esc(titulo_en)}</h1>
        {meta_item}
        <ul class="tags" role="list">{tags}</ul>
      </header>

{intro}{portada(p, pre)}

{cuerpo}{nda}

{pager}
    </article>
  </main>

  <footer class="footer">
    <p>© <span id="year">2026</span> Ana López Canellas</p>
    <a href="#main"><span{comun_attr("back_to_top")}>Back to top</span> <span aria-hidden="true">↑</span></a>
  </footer>

  <script src="../js/i18n-proyectos.js"></script>
  <script src="../js/i18n.js"></script>
  <script src="../js/main.js"></script>
</body>
</html>
'''


# ----------------------------------------------------------------------------------------------
# Proceso principal
# ----------------------------------------------------------------------------------------------

def leer_orden():
    ruta = os.path.join(FICHAS, "orden.txt")
    if not os.path.exists(ruta):
        raise FichaError("falta fichas/orden.txt (un nombre de proyecto por línea)")
    orden = []
    for l in leer(ruta).split("\n"):
        l = l.split("#")[0].strip().replace(".html", "")
        if l:
            if l in orden:
                raise FichaError(f"fichas/orden.txt: '{l}' está repetido")
            orden.append(l)
    return orden


def tarjeta_existente(index_html, slug):
    m = re.search(r'      <a class="card" href="proyectos/%s\.html"[^>]*>.*?      </a>\n' % re.escape(slug), index_html, re.S)
    return m.group(0) if m else None


def destino_pager(slug, proyectos, index_html):
    """Texto y clave del título de un proyecto, para los enlaces Anterior/Siguiente."""
    if slug in proyectos:
        p = proyectos[slug]
        return {"slug": slug, "en": p.titulo[0], "attr": p.T("titulo", *p.titulo)}
    tj = tarjeta_existente(index_html, slug)
    if not tj:
        raise FichaError(f"'{slug}' está en orden.txt pero no tiene ficha ni tarjeta en index.html")
    m = re.search(r"<h3([^>]*)>(.*?)</h3>", tj, re.S)
    return {"slug": slug, "en": html.unescape(m.group(2)), "attr": re.search(r' data-i18n="[^"]*"', m.group(1)).group(0) if 'data-i18n="' in m.group(1) else ""}


def main():
    cargar_es_comun()
    orden = leer_orden()
    fichas = {}
    for f in sorted(os.listdir(FICHAS)):
        if f.endswith(".txt") and not f.startswith("_") and f != "orden.txt":
            p = Proyecto(os.path.join(FICHAS, f))
            fichas[p.slug] = p
    for slug in fichas:
        if slug not in orden:
            AVISOS.append(f"fichas/{slug}.txt existe pero no está en fichas/orden.txt: no aparecerá en la web")
    proyectos = {s: fichas[s] for s in orden if s in fichas}
    index_html = leer(INDEX)
    for s in orden:
        if s not in proyectos and not os.path.exists(os.path.join(PROY, s + ".html")):
            raise FichaError(f"'{s}' está en orden.txt pero no existe fichas/{s}.txt ni proyectos/{s}.html")

    paginas = {}
    for i, slug in enumerate(orden):
        if slug not in proyectos:
            continue
        ant = destino_pager(orden[(i - 1) % len(orden)], proyectos, index_html)
        sig = destino_pager(orden[(i + 1) % len(orden)], proyectos, index_html)
        destino = os.path.join(PROY, slug + ".html")
        if os.path.exists(destino) and "data-gate" in leer(destino):
            AVISOS.append(f"{slug}: está protegido con contraseña; no se regenera (ejecuta 'quitar' en tools/proteger.py y vuelve a construir)")
            continue
        paginas[slug] = pagina(proyectos[slug], ant, sig)

    # tarjetas de Inicio
    tarjetas = []
    for slug in orden:
        existente = tarjeta_existente(index_html, slug)
        if slug in proyectos and not (existente and "data-label-original" in existente):
            tarjetas.append(tarjeta(proyectos[slug]))
        elif existente:
            tarjetas.append(existente)
        else:
            raise FichaError(f"no puedo crear la tarjeta de '{slug}'")
    m = re.search(r'(      <div class="cards">\n).*?(      </div>\n    </section>)', index_html, re.S)
    if not m:
        raise FichaError('no encuentro <div class="cards"> en index.html')
    nuevo_index = index_html[:m.end(1)] + "".join(tarjetas) + index_html[m.start(2):]

    # enlaces Anterior/Siguiente de las páginas hechas a mano
    manuales = {}
    for i, slug in enumerate(orden):
        if slug in proyectos:
            continue
        ruta = os.path.join(PROY, slug + ".html")
        txt = leer(ruta)
        ant = destino_pager(orden[(i - 1) % len(orden)], proyectos, index_html)
        sig = destino_pager(orden[(i + 1) % len(orden)], proyectos, index_html)

        def enlace(dest, lado):
            t = f'<span{dest["attr"]}>{esc(dest["en"])}</span>' if dest["attr"] else esc(dest["en"])
            if lado == "ant":
                lab = f'<span><span aria-hidden="true">← </span><span{comun_attr("previous")}>Previous</span></span>'
            else:
                lab = f'<span><span{comun_attr("next")}>Next</span><span aria-hidden="true"> →</span></span>'
            return f'        <a href="{dest["slug"]}.html">{lab}{t}</a>'
        nav = ('<nav class="pager" aria-label="More projects"' + comun_attr("more_projects", "aria-label") + ">\n"
               + enlace(ant, "ant") + "\n" + enlace(sig, "sig") + "\n      </nav>")
        nuevo, n = re.subn(r'<nav class="pager".*?</nav>', lambda _m: nav, txt, count=1, flags=re.S)
        if n != 1:
            AVISOS.append(f"{slug}: no encuentro el bloque <nav class=\"pager\"> para actualizar Anterior/Siguiente")
            continue
        # la página hecha a mano también necesita cargar las traducciones de proyectos
        if "i18n-proyectos.js" not in nuevo:
            nuevo = nuevo.replace('<script src="../js/i18n.js"></script>', '<script src="../js/i18n-proyectos.js"></script>\n  <script src="../js/i18n.js"></script>', 1)
        manuales[slug] = nuevo
    if "i18n-proyectos.js" not in nuevo_index:
        nuevo_index = nuevo_index.replace('<script src="js/i18n.js"></script>', '<script src="js/i18n-proyectos.js"></script>\n  <script src="js/i18n.js"></script>', 1)

    # traducciones
    reg = {}
    for p in proyectos.values():
        reg.update(p.reg)
    reg.update(ES_COMUN_USADAS)
    import json
    cuerpo_js = ("// AUTOGENERADO por tools/construir.py a partir de las fichas. NO editar a mano: se pierde al volver a construir.\n"
                 "window.I18N_PROYECTOS = " + json.dumps(reg, ensure_ascii=False, indent=2, sort_keys=True) + ";\n")

    if AVISOS:
        print("AVISOS:")
        for a in AVISOS:
            print("  -", a)
    if SOLO_COMPROBAR:
        print(f"\nFichas correctas: {len(proyectos)} proyecto(s). No se ha escrito nada.")
        return
    for slug, txt in paginas.items():
        escribir(os.path.join(PROY, slug + ".html"), txt)
    for slug, txt in manuales.items():
        escribir(os.path.join(PROY, slug + ".html"), txt)
    escribir(INDEX, nuevo_index)
    escribir(I18N_PROY, cuerpo_js)
    print(f"\nListo: {len(paginas)} página(s) generada(s), {len(manuales)} hecha(s) a mano con enlaces actualizados, "
          f"{len(tarjetas)} tarjetas, {len(reg)} traducciones.")
    print("Siguiente paso: python3 tools/comprobar-idiomas.py")


if __name__ == "__main__":
    try:
        main()
    except FichaError as e:
        print("\nERROR en las fichas:", e)
        sys.exit(1)
