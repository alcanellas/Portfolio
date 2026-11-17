# Publicar el portfolio y conectar tu dominio

El portfolio es una web estática (solo archivos): no necesita servidor ni base de datos. Cualquier servicio de alojamiento estático sirve. Las pantallas y los nombres de los menús de estos servicios cambian con el tiempo, así que usa estos pasos como guía y sigue las instrucciones de cada servicio si algo no coincide.

## 0. Antes de nada

1. **Aprobación:** confirma con tu equipo si necesitas aprobación interna para publicar los proyectos (ver pendientes en `README.md`).
2. **Correo:** tu correo personal queda visible en *Sobre mí* y en los botones de los proyectos. Si prefieres uno solo para el portfolio, cámbialo en `sobre-mi.html` (el texto del botón, su atributo `data-copy` y el bloque `noscript`) y en los 5 proyectos de cliente (`mailto:` del botón "Email me").
3. **Revisión:** haz las comprobaciones de accesibilidad de `GUIA.md` (teclado, Lighthouse, WAVE).
4. **Contenido pendiente:** texto e imagen de Workshops y los datos que figuran en `README.md → Pendiente`.

## 1. Preparar la carpeta que se sube

Si has cambiado alguna ficha, primero ejecuta `python3 tools/construir.py` para regenerar las páginas.

**No subas la carpeta del proyecto tal cual:** contiene `privado/` con los originales de las capturas. Genera una copia limpia:

```
cd ~/Desktop/"Portfolio ALC"
bash tools/preparar-publicacion.sh
```

Crea `~/Desktop/Portfolio ALC - publicar` sin `privado/`, `tools/`, `fichas/` ni los `.md`, te lista su contenido y avisa si algo enlazado no existe. **Sube siempre esa carpeta**, no la original. Repite el comando cada vez que cambies algo.

## 2. Elegir dónde publicar

| Opción | Cuándo conviene |
|---|---|
| **Netlify** (netlify.com) | Lo más sencillo: arrastras la carpeta a la página y queda publicada. Plan gratuito. |
| **Cloudflare Pages** (pages.cloudflare.com) | Plan gratuito generoso; permite subir la carpeta directamente. Si ya tienes el dominio en Cloudflare, es lo más cómodo. |
| **Vercel** (vercel.com) | Parecido a Netlify. |
| **GitHub Pages** | Requiere crear un repositorio y usar git. Más pasos; conviene si ya trabajas con GitHub. |

### Con Netlify (arrastrar y soltar)

1. Entra en `app.netlify.com/drop` (necesitas una cuenta; puedes crearla con tu correo).
2. Arrastra la carpeta `Portfolio ALC - publicar` a la zona de subida.
3. Netlify te da una dirección del tipo `algo.netlify.app`. Ábrela y comprueba las 8 páginas, el modo oscuro y el botón de copiar el correo.
4. Para actualizar más adelante: vuelve a ejecutar el script del punto 1 y sube la carpeta de nuevo (en el panel del sitio, *Deploys*).

## 3. Conectar tu dominio

Si todavía no tienes dominio, se compra en un registrador (por ejemplo Namecheap, Porkbun, Cloudflare Registrar u otro de tu confianza). Un dominio `.com` cuesta unos 10-15 € al año.

1. En el servicio donde has publicado (por ejemplo Netlify), busca **Domain management** o **Custom domains** y añade tu dominio (por ejemplo `analopezcanellas.com`).
2. El servicio te indicará qué **registros DNS** crear. Normalmente:
   - Para `www.tudominio.com`: un registro **CNAME** hacia la dirección que te dan (`algo.netlify.app`).
   - Para el dominio sin `www` (`tudominio.com`): un registro **A** (o **ALIAS/ANAME**) con la dirección que te indiquen.
   - Alternativa más simple: cambiar los **nameservers** del dominio a los del servicio, si lo ofrece.
3. Esos registros se crean en el panel **DNS del registrador** donde compraste el dominio.
4. Espera a que se propague (de unos minutos a unas horas). Puedes comprobarlo en dnschecker.org.
5. Activa el **HTTPS** (certificado gratuito); en Netlify y Cloudflare Pages es automático cuando el dominio queda verificado.
6. Haz que una de las dos versiones redirija a la otra (con o sin `www`), para no tener dos direcciones.

## 4. Después de publicar

- **Idiomas:** prueba el selector EN | ES y las direcciones `tudominio.com/?lang=es` y `?lang=en`. El español se aplica con JavaScript: los buscadores indexan la versión en inglés. Si quieres que Google indexe también el español, habría que crear páginas separadas (`/es/…`); es más trabajo de mantenimiento.

- Abre la web en el móvil y en otro navegador. Prueba el modo claro y oscuro.
- Comprueba que **no** se puede abrir `tudominio.com/privado/` (debe dar error 404). Si abre, has subido la carpeta equivocada.
- Si no quieres que Google indexe tus proyectos, cambia `<meta name="robots" content="index, follow">` a `noindex, nofollow` en todas las páginas, o pide protección por contraseña a nivel de hosting.
- Pasa Lighthouse sobre la dirección real.
- Añade la dirección a tu LinkedIn y a tu firma de correo.

## 5. Mantenimiento

1. Edita en `~/Desktop/Portfolio ALC` (la carpeta de trabajo).
2. Prueba en local abriendo `index.html`.
3. Ejecuta `bash tools/preparar-publicacion.sh`.
4. Sube la carpeta `Portfolio ALC - publicar` de nuevo.
5. Si usas Git, el `.gitignore` ya excluye `privado/`.
