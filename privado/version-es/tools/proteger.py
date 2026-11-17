#!/usr/bin/env python3
"""
Protege con contraseña las páginas de proyecto del portfolio.

El contenido de <main> se cifra (AES-256 + PBKDF2) y solo se descifra en el
navegador cuando la persona introduce la contraseña. No necesita instalar nada:
solo Python 3 y openssl, que ya vienen con macOS.

Uso (desde la carpeta del portfolio):
  python3 tools/proteger.py estado                      # qué proyectos están protegidos
  python3 tools/proteger.py proteger <proyecto>         # protege proyectos/<proyecto>.html
  python3 tools/proteger.py quitar <proyecto>           # vuelve a dejarlo público

<proyecto> es el nombre del archivo sin .html, por ejemplo: retail-ecommerce

IMPORTANTE
- El original sin cifrar se guarda en privado/proyectos/. Edita ahí el contenido y
  vuelve a ejecutar "proteger". NO subas la carpeta privado/ al publicar la web.
- Solo se cifra el texto de la página. Las imágenes son archivos normales: cualquiera
  que conozca su dirección puede abrirlas. Usa imágenes ya anonimizadas.
- Usa una contraseña larga (4 palabras al azar o 14+ caracteres): el cifrado es tan
  fuerte como la contraseña.
"""
import base64, getpass, os, re, shutil, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROY = os.path.join(RAIZ, "proyectos")
PRIV = os.path.join(RAIZ, "privado", "proyectos")
INDEX = os.path.join(RAIZ, "index.html")
ITER = 600000
MARCA = "ALCOK:"
MAIN_RE = re.compile(r'(<main id="main" tabindex="-1">)(.*?)(</main>)', re.S)
LOCK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<rect x="4" y="11" width="16" height="10" rx="3"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>')
ETIQUETA = "Protegido con contraseña"


def leer(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def escribir(p, s):
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)


def error(msg):
    print("Error: " + msg)
    sys.exit(1)


def esta_protegida(html):
    return "data-gate" in html


def cifrar(texto, password):
    env = dict(os.environ, ALC_PW=password)
    r = subprocess.run(
        ["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-iter", str(ITER), "-md", "sha256",
         "-salt", "-pass", "env:ALC_PW"],
        input=(MARCA + texto).encode("utf-8"), capture_output=True, env=env)
    if r.returncode != 0:
        error("openssl falló: " + r.stderr.decode(errors="replace"))
    return base64.b64encode(r.stdout).decode("ascii")


def puerta(payload):
    return f'''
    <section class="gate" data-gate data-iter="{ITER}" data-payload="{payload}">
      <div class="gate-box">
        <span class="gate-lock">{LOCK}</span>
        <h1>Proyecto protegido</h1>
        <p>Este proyecto es confidencial. Introduce la contraseña que te he facilitado para verlo.</p>
        <form class="gate-form" novalidate>
          <label for="gate-pw">Contraseña</label>
          <input id="gate-pw" name="password" type="password" autocomplete="current-password" required>
          <button type="submit">Ver proyecto</button>
          <p class="gate-error" role="alert" hidden>Contraseña incorrecta. Inténtalo de nuevo.</p>
        </form>
        <p class="gate-help">¿No tienes la contraseña? <a href="mailto:alcanellass@gmail.com">Solicítame acceso</a>.</p>
        <p class="gate-help"><a href="../index.html">Volver a proyectos</a></p>
        <noscript><p class="gate-error">Para ver este proyecto necesitas activar JavaScript.</p></noscript>
      </div>
    </section>
  '''


def tarjeta(html, slug, texto, original=None):
    patron = re.compile(r'(<a class="card" href="proyectos/%s\.html">.*?</a>)' % re.escape(slug), re.S)
    m = patron.search(html)
    if not m:
        return html
    bloque = m.group(1)
    lab = re.search(r'<span class="conf-label"(?: data-label-original="([^"]*)")?>(.*?)</span>', bloque)
    if not lab:
        return html
    if original is None:
        original = lab.group(1) or lab.group(2)
        nuevo = f'<span class="conf-label" data-label-original="{original}">{texto}</span>'
    else:
        nuevo = f'<span class="conf-label">{original}</span>'
    return html.replace(bloque, bloque.replace(lab.group(0), nuevo, 1), 1)


def pedir_password():
    while True:
        p1 = getpass.getpass("Contraseña (no se verá al escribir): ")
        if len(p1) < 12:
            print("Demasiado corta: usa al menos 12 caracteres (mejor 4 palabras al azar).")
            continue
        if p1 != getpass.getpass("Repítela: "):
            print("No coinciden.")
            continue
        return p1


def proteger(slug):
    destino = os.path.join(PROY, slug + ".html")
    fuente = os.path.join(PRIV, slug + ".html")
    if not os.path.exists(destino) and not os.path.exists(fuente):
        error(f"no existe proyectos/{slug}.html")
    if os.path.exists(fuente):
        original = leer(fuente)
    else:
        original = leer(destino)
        if esta_protegida(original):
            error("esa página ya está protegida y no hay original en privado/. No se puede recuperar.")
    m = MAIN_RE.search(original)
    if not m:
        error('no encuentro <main id="main" tabindex="-1"> en el original')
    password = os.environ.get("ALC_PASSWORD") or pedir_password()
    if len(password) < 12:
        error("la contraseña debe tener al menos 12 caracteres")
    os.makedirs(PRIV, exist_ok=True)
    escribir(fuente, original)
    payload = cifrar(m.group(2), password)
    html = original[:m.start(2)] + puerta(payload) + original[m.end(2):]
    if "unlock.js" not in html:
        html = html.replace("</body>", '  <script src="../js/unlock.js" defer></script>\n</body>', 1)
    if "gate-robots" not in html:
        html = html.replace("</head>", '  <meta name="robots" content="noindex" data-gate-robots>\n</head>', 1)
    escribir(destino, html)
    idx = leer(INDEX)
    escribir(INDEX, tarjeta(idx, slug, ETIQUETA))
    print(f"Protegido: proyectos/{slug}.html")
    print(f"Original sin cifrar guardado en: privado/proyectos/{slug}.html  (no lo subas a internet)")


def quitar(slug):
    fuente = os.path.join(PRIV, slug + ".html")
    destino = os.path.join(PROY, slug + ".html")
    if not os.path.exists(fuente):
        error(f"no hay original en privado/proyectos/{slug}.html; ¿está protegida?")
    shutil.copyfile(fuente, destino)
    os.remove(fuente)
    idx = leer(INDEX)
    m = re.search(r'<a class="card" href="proyectos/%s\.html">.*?</a>' % re.escape(slug), idx, re.S)
    if m:
        lab = re.search(r'data-label-original="([^"]*)"', m.group(0))
        if lab:
            idx = tarjeta(idx, slug, "", original=lab.group(1))
            escribir(INDEX, idx)
    print(f"Publicado de nuevo sin contraseña: proyectos/{slug}.html")


def estado():
    for f in sorted(os.listdir(PROY)):
        if f.endswith(".html"):
            print(("PROTEGIDO  " if esta_protegida(leer(os.path.join(PROY, f))) else "público    ") + f)


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ("estado", "proteger", "quitar") or (a[0] != "estado" and len(a) != 2):
        print(__doc__)
        sys.exit(1)
    if a[0] == "estado":
        estado()
    elif a[0] == "proteger":
        proteger(a[1].replace(".html", ""))
    else:
        quitar(a[1].replace(".html", ""))


if __name__ == "__main__":
    main()
