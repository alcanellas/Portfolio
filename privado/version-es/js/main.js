document.getElementById('year').textContent = new Date().getFullYear();

// Tema claro / oscuro: respeta el sistema y recuerda la elección de la persona
(function () {
  const root = document.documentElement;
  const btn = document.querySelector('.theme-toggle');
  const media = window.matchMedia('(prefers-color-scheme: dark)');
  const COLORS = { light: '#FFFFFF', dark: '#000000' };

  function apply(theme) {
    root.setAttribute('data-theme', theme);
    if (btn) btn.setAttribute('aria-pressed', String(theme === 'dark'));
    document.querySelectorAll('meta[name="theme-color"]').forEach(function (m) {
      m.removeAttribute('media');
      m.setAttribute('content', COLORS[theme]);
    });
  }
  function saved() {
    try { return localStorage.getItem('theme'); } catch (e) { return null; }
  }

  apply(saved() || (media.matches ? 'dark' : 'light'));

  if (btn) {
    btn.addEventListener('click', function () {
      const next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      apply(next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }
  media.addEventListener('change', function (e) {
    if (!saved()) apply(e.matches ? 'dark' : 'light');
  });
})();

// Portadas: si la imagen no existe, se quita y queda la portada de respaldo (candado)
function initCovers(root) {
  (root || document).querySelectorAll('.cover-confidential > img').forEach(function (img) {
    function drop() { img.remove(); }
    if (img.complete && img.naturalWidth === 0) drop();
    img.addEventListener('error', drop);
  });
}
window.initCovers = initCovers;
initCovers(document);

// Copiar el correo al portapapeles al hacer clic
function copiarTexto(texto) {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(texto).then(function () { return true; }, function () { return copiarFallback(texto); });
  }
  return Promise.resolve(copiarFallback(texto));
}
function copiarFallback(texto) {
  var area = document.createElement('textarea');
  area.value = texto;
  area.setAttribute('readonly', '');
  area.style.position = 'fixed';
  area.style.opacity = '0';
  document.body.appendChild(area);
  area.select();
  var ok = false;
  try { ok = document.execCommand('copy'); } catch (e) {}
  document.body.removeChild(area);
  return ok;
}
document.querySelectorAll('[data-copy]').forEach(function (btn) {
  var estado = document.getElementById(btn.getAttribute('aria-describedby'));
  btn.addEventListener('click', function () {
    copiarTexto(btn.dataset.copy).then(function (ok) {
      estado.textContent = ok ? 'Correo copiado al portapapeles' : 'No se pudo copiar; escríbelo a mano: ' + btn.dataset.copy;
      btn.classList.toggle('copied', !!ok);
      clearTimeout(btn._t);
      btn._t = setTimeout(function () { estado.textContent = ''; btn.classList.remove('copied'); }, 3500);
    });
  });
});

// Imágenes para modo oscuro: si no existe el archivo "-dark", se mantiene la versión clara
document.querySelectorAll('.theme-pair .img-dark').forEach(function (img) {
  var par = img.closest('.theme-pair');
  img.addEventListener('error', function () { par.classList.add('no-dark'); });
});


// Carrusel: flechas, puntos y diapositiva activa (sin JS sigue funcionando deslizando)
document.querySelectorAll('.carousel').forEach(function (car) {
  var pista = car.querySelector('.carousel-track');
  var diapos = pista.querySelectorAll('.carousel-slide');
  var prev = car.querySelector('.carousel-prev');
  var next = car.querySelector('.carousel-next');
  var puntos = car.querySelector('.carousel-dots');
  var estado = car.querySelector('.carousel-status');
  var botones = [];
  var ultimo = -1;
  function indice() { return Math.min(Math.max(Math.round(pista.scrollLeft / (diapos[0].offsetWidth + 16)), 0), diapos.length - 1); }
  function ir(i) { pista.scrollTo({ left: i * (diapos[0].offsetWidth + 16), behavior: 'smooth' }); }
  diapos.forEach(function (d, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'carousel-dot';
    b.setAttribute('aria-label', 'Ir a la diapositiva ' + (i + 1) + ' de ' + diapos.length);
    b.addEventListener('click', function () { ir(i); });
    puntos.appendChild(b);
    botones.push(b);
  });
  function actualizar() {
    var i = indice();
    diapos.forEach(function (d, n) { d.classList.toggle('is-active', n === i); });
    botones.forEach(function (b, n) { if (n === i) b.setAttribute('aria-current', 'true'); else b.removeAttribute('aria-current'); });
    prev.disabled = i === 0;
    next.disabled = i === diapos.length - 1;
    if (i !== ultimo) { if (ultimo !== -1) estado.textContent = 'Diapositiva ' + (i + 1) + ' de ' + diapos.length; ultimo = i; }
  }
  prev.addEventListener('click', function () { ir(indice() - 1); });
  next.addEventListener('click', function () { ir(indice() + 1); });
  pista.addEventListener('scroll', function () { clearTimeout(pista._t); pista._t = setTimeout(actualizar, 60); });
  window.addEventListener('resize', actualizar);
  if (diapos.length < 2) return;
  prev.hidden = next.hidden = puntos.hidden = false;
  car.classList.add('is-ready');
  actualizar();
});


// Tarjetas de aplicación en proyectos: abren un diálogo modal con su carrusel
document.querySelectorAll('[data-open]').forEach(function (btn) {
  var dlg = document.getElementById(btn.dataset.open);
  btn.addEventListener('click', function () {
    dlg.showModal();
    var pista = dlg.querySelector('.carousel-track');
    pista.scrollTo({ left: 0, behavior: 'instant' });
    window.dispatchEvent(new Event('resize'));
  });
  dlg.querySelector('.app-dialog-close').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
});
