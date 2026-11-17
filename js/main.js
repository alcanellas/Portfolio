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
      estado.textContent = ok ? i18n.t('copied') : i18n.t('copyFail') + btn.dataset.copy;
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
    b.setAttribute('aria-label', i18n.t('goSlide', i + 1, diapos.length));
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
    if (i !== ultimo) { if (ultimo !== -1) estado.textContent = i18n.t('slide', i + 1, diapos.length); ultimo = i; }
  }
  window.addEventListener('alc:lang', function () {
    botones.forEach(function (b, n) { b.setAttribute('aria-label', i18n.t('goSlide', n + 1, diapos.length)); });
  });
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

// Menú lateral "Contents" en las páginas de proyecto: una entrada por sección, la actual queda marcada al hacer scroll
(function () {
  if (!document.querySelector('.project-body')) return;
  const heads = Array.from(document.querySelectorAll('.project-intro > h2, .project-body > section > h2, .gallery > section > h3:first-child'));
  if (heads.length < 2) return;
  const nav = document.createElement('nav');
  nav.className = 'toc';
  const title = document.createElement('p');
  title.className = 'toc-title';
  title.id = 'toc-title';
  nav.setAttribute('aria-labelledby', 'toc-title');
  const list = document.createElement('ul');
  const links = heads.map(function (h, n) {
    if (!h.id) h.id = 'sec-' + (n + 1);
    const sec = h.closest('section');
    sec.style.scrollMarginTop = '120px';
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#' + h.id;
    li.appendChild(a);
    list.appendChild(li);
    return a;
  });
  nav.append(title, list);
  document.body.appendChild(nav);
  function textos() {
    title.textContent = i18n.t('contents');
    links.forEach(function (a, n) { a.textContent = heads[n].textContent; });
  }
  function actual() {
    let k = 0;
    heads.forEach(function (h, n) { if (h.getBoundingClientRect().top < window.innerHeight * 0.4) k = n; });
    links.forEach(function (a, n) { if (n === k) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
  }
  window.addEventListener('alc:lang', textos);
  window.addEventListener('scroll', actual, { passive: true });
  window.addEventListener('resize', actual);
  textos();
  actual();
})();

// Filtros de la lista de proyectos (Inicio): por empresa, año y tipo de cliente. Se crean a partir de los data-* de cada tarjeta
(function () {
  const cards = Array.from(document.querySelectorAll('.cards > .card[data-year]'));
  const section = document.getElementById('trabajo');
  if (!section || cards.length < 2) return;
  const lang = function () { return i18n.get() === 'es' ? 'es' : 'en'; };
  const GROUPS = [
    { key: 'company', min: 2, label: 'fCompany', value: function (c) { return c.dataset.company; }, text: function (c) { return c.dataset.company; } },
    { key: 'year', label: 'fYear', value: function (c) { return c.dataset.year; }, text: function (c) { return c.dataset.year; }, desc: true },
    { key: 'sector', label: 'fSector', value: function (c) { return c.dataset.sector; }, text: function (c) { return lang() === 'es' && c.dataset.sectorEs ? c.dataset.sectorEs : c.dataset.sector; } }
  ];
  const active = {};
  const nav = document.createElement('nav');
  nav.className = 'filters';
  nav.setAttribute('aria-labelledby', 'filters-title');
  const title = document.createElement('h3');
  title.className = 'filters-title';
  title.id = 'filters-title';
  const status = document.createElement('p');
  status.className = 'sr-only';
  status.setAttribute('role', 'status');
  const empty = document.createElement('p');
  empty.className = 'filters-empty';
  empty.hidden = true;
  const all = document.createElement('button');
  all.type = 'button';
  all.className = 'filter-btn filter-all';
  all.addEventListener('click', function () { GROUPS.forEach(function (g) { delete active[g.key]; }); apply(); });
  nav.append(title, all);
  const buttons = [];
  GROUPS.forEach(function (g) {
    const seen = {};
    cards.forEach(function (c) { const v = g.value(c); if (v && !seen[v]) seen[v] = c; });
    const values = Object.keys(seen);
    // Un grupo con menos opciones que 'min' no se muestra (empresa: hasta que haya al menos dos)
    if (values.length < (g.min || 1)) return;
    values.sort(function (a, b) { return g.desc ? b.localeCompare(a) : a.localeCompare(b); });
    const grp = document.createElement('div');
    grp.className = 'filter-group';
    grp.setAttribute('role', 'group');
    const gt = document.createElement('span');
    gt.className = 'filter-group-title';
    const gv = document.createElement('span');
    gv.className = 'filter-group-value';
    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'filter-group-btn';
    toggle.id = 'fg-' + g.key;
    toggle.setAttribute('aria-expanded', 'false');
    toggle.setAttribute('aria-controls', 'fl-' + g.key);
    toggle.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>';
    toggle.prepend(gt, gv);
    grp.setAttribute('aria-labelledby', toggle.id);
    const ul = document.createElement('ul');
    ul.id = 'fl-' + g.key;
    ul.setAttribute('role', 'list');
    ul.hidden = true;
    toggle.addEventListener('click', function () {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      ul.hidden = !open;
      grp.classList.toggle('is-open', open);
    });
    values.forEach(function (v) {
      const li = document.createElement('li');
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'filter-btn';
      b.addEventListener('click', function () {
        if (active[g.key] === v) delete active[g.key]; else active[g.key] = v;
        apply();
      });
      li.appendChild(b);
      ul.appendChild(li);
      buttons.push({ b: b, g: g, v: v, sample: seen[v] });
    });
    grp.append(toggle, ul);
    nav.appendChild(grp);
    g.titleEl = gt;
    g.valueEl = gv;
  });
  section.classList.add('has-filters');
  section.insertBefore(nav, section.querySelector('.cards'));
  section.appendChild(status);
  section.querySelector('.cards').after(empty);

  function labels() {
    title.textContent = i18n.t('filterTitle');
    all.textContent = i18n.t('fAll');
    GROUPS.forEach(function (g) { if (g.titleEl) g.titleEl.textContent = i18n.t(g.label); });
    buttons.forEach(function (x) {
      const n = cards.filter(function (c) { return x.g.value(c) === x.v; }).length;
      x.b.textContent = '';
      x.b.append(x.g.text(x.sample));
      const k = document.createElement('span');
      k.className = 'filter-count';
      k.textContent = n;
      x.b.append(k);
    });
    empty.textContent = i18n.t('fNone');
  }
  function apply() {
    let shown = 0;
    cards.forEach(function (c) {
      const ok = GROUPS.every(function (g) { return !active[g.key] || g.value(c) === active[g.key]; });
      c.hidden = !ok;
      if (ok) shown++;
    });
    GROUPS.forEach(function (g) { if (g.valueEl) g.valueEl.textContent = ''; });
    buttons.forEach(function (x) {
      const on = active[x.g.key] === x.v;
      x.b.setAttribute('aria-pressed', String(on));
      if (on) x.g.valueEl.textContent = x.g.text(x.sample);
    });
    all.setAttribute('aria-pressed', String(!Object.keys(active).length));
    empty.hidden = shown > 0;
    status.textContent = i18n.t('fShowing', shown, cards.length);
  }
  window.addEventListener('alc:lang', function () { labels(); apply(); });
  labels();
  apply();
  status.textContent = '';
})();

/* Sobre mí: fotos apiladas; pasa una delante al pasar el ratón o al tocar */
(function () {
  const stack = document.getElementById('prints');
  if (!stack) return;
  const which = function (el) { return el.closest('.is-front') ? 'front' : el.closest('.is-back') ? 'back' : null; };
  if (matchMedia('(hover: hover)').matches) {
    stack.addEventListener('mouseover', function (e) { const w = which(e.target); if (w === 'back') stack.dataset.front = 'back'; else if (w === 'front') delete stack.dataset.front; });
    stack.addEventListener('mouseleave', function () { delete stack.dataset.front; });
  } else {
    stack.addEventListener('click', function (e) { const w = which(e.target); if (!w) return; if (w === 'back' && stack.dataset.front !== 'back') stack.dataset.front = 'back'; else delete stack.dataset.front; });
  }
})();

/* Fotografía de viajes: carrusel en movimiento continuo; se pausa con el ratón, con el foco o con el botón */
(function () {
  const box = document.getElementById('marquee');
  if (!box || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  const set = box.querySelector('.marquee-set');
  const btn = box.parentNode.querySelector('.marquee-toggle');
  const track = document.createElement('div');
  track.className = 'marquee-track';
  const copy = set.cloneNode(true);
  copy.setAttribute('aria-hidden', 'true');
  copy.querySelectorAll('img').forEach(function (img) { img.alt = ''; img.removeAttribute('data-i18n-alt'); img.loading = 'lazy'; });
  box.insertBefore(track, set);
  track.appendChild(set);
  track.appendChild(copy);
  box.classList.add('is-moving');
  btn.innerHTML = '<svg class="i-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg><svg class="i-play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>';
  btn.hidden = false;
  function label() { btn.setAttribute('aria-label', i18n.t(box.classList.contains('is-paused') ? 'playCarousel' : 'pauseCarousel')); }
  btn.addEventListener('click', function () {
    const paused = box.classList.toggle('is-paused');
    btn.setAttribute('aria-pressed', String(paused));
    label();
  });
  window.addEventListener('alc:lang', label);
  label();
})();

// Móvil: el botón "Links" abre y cierra las opciones (LinkedIn, correo, tema e idioma)
(function () {
  const nav = document.querySelector('.nav');
  const btn = document.querySelector('.menu-links-btn');
  if (!nav || !btn) return;
  function set(open) {
    nav.classList.toggle('tools-open', open);
    btn.setAttribute('aria-expanded', String(open));
  }
  btn.addEventListener('click', function () { set(btn.getAttribute('aria-expanded') !== 'true'); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') { set(false); btn.focus(); }
  });
})();

// Portada de Inicio: sin scroll. Solo se pasa a Proyectos con "View projects" o con el menú, y solo se vuelve con la casita
(function () {
  const hero = document.querySelector('.hero');
  if (!hero) return;
  const root = document.documentElement;
  function hide() {
    root.classList.add('hero-gone');
    try { sessionStorage.setItem('heroGone', '1'); } catch (e) {}
    history.replaceState(null, '', '#trabajo');
    window.scrollTo({ top: 0, behavior: 'instant' });
  }
  function show() {
    root.classList.remove('hero-gone');
    try { sessionStorage.removeItem('heroGone'); } catch (e) {}
    history.replaceState(null, '', '#inicio');
    window.scrollTo({ top: 0, behavior: 'instant' });
  }
  document.querySelectorAll('a[href$="#trabajo"]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); hide(); });
  });
  document.querySelectorAll('a[href$="#inicio"]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); show(); });
  });
  window.addEventListener('hashchange', function () {
    if (location.hash === '#trabajo') hide();
    else if (location.hash === '#inicio') show();
  });
})();
