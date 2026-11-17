// Descifra las páginas de proyecto protegidas con contraseña (generadas con tools/proteger.py)
(function () {
  var gate = document.querySelector('[data-gate]');
  if (!gate) return;

  var main = document.getElementById('main');
  var form = gate.querySelector('form');
  var input = gate.querySelector('input');
  var button = gate.querySelector('button');
  var errorBox = gate.querySelector('.gate-error');
  var KEY = 'alc-gate';
  var MARCA = 'ALCOK:';

  function b64ToBytes(b64) {
    var bin = atob(b64);
    var out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }

  // Formato de openssl enc: "Salted__" + sal (8 bytes) + datos cifrados
  async function descifrar(password) {
    var raw = b64ToBytes(gate.dataset.payload);
    var salt = raw.slice(8, 16);
    var data = raw.slice(16);
    var base = await crypto.subtle.importKey('raw', new TextEncoder().encode(password), 'PBKDF2', false, ['deriveBits']);
    var bits = await crypto.subtle.deriveBits(
      { name: 'PBKDF2', salt: salt, iterations: parseInt(gate.dataset.iter, 10), hash: 'SHA-256' }, base, 384);
    var key = await crypto.subtle.importKey('raw', bits.slice(0, 32), { name: 'AES-CBC' }, false, ['decrypt']);
    var plain = await crypto.subtle.decrypt({ name: 'AES-CBC', iv: bits.slice(32, 48) }, key, data);
    var text = new TextDecoder().decode(plain);
    if (text.indexOf(MARCA) !== 0) throw new Error('contraseña incorrecta');
    return text.slice(MARCA.length);
  }

  function mostrar(html, password) {
    main.innerHTML = html;
    if (window.i18n) window.i18n.apply(main);
    try { sessionStorage.setItem(KEY, password); } catch (e) {}
    if (window.initCovers) window.initCovers(main);
    var h1 = main.querySelector('h1');
    if (h1) { h1.setAttribute('tabindex', '-1'); h1.focus(); }
    window.scrollTo(0, 0);
  }

  async function intentar(password, silencioso) {
    try {
      mostrar(await descifrar(password), password);
      return true;
    } catch (e) {
      if (!silencioso) {
        errorBox.hidden = false;
        input.setAttribute('aria-invalid', 'true');
        input.focus();
        input.select();
      }
      return false;
    }
  }

  if (!window.crypto || !crypto.subtle) {
    errorBox.hidden = false;
    errorBox.textContent = i18n.t('noCrypto');
    return;
  }

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (!input.value) { errorBox.hidden = false; input.focus(); return; }
    errorBox.hidden = true;
    input.removeAttribute('aria-invalid');
    button.disabled = true;
    button.textContent = i18n.t('decrypting');
    var ok = await intentar(input.value, false);
    if (!ok) { button.disabled = false; button.textContent = i18n.t('viewProject'); }
  });

  // Si ya se desbloqueó en esta pestaña, no vuelve a pedir la contraseña
  var guardada = null;
  try { guardada = sessionStorage.getItem(KEY); } catch (e) {}
  if (guardada) intentar(guardada, true);
})();
