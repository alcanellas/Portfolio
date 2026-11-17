// Idioma de la web: inglés y español.
// El HTML está escrito en INGLÉS (es la versión por defecto y la que ven los buscadores y quien no tiene JavaScript).
// Aquí está el ESPAÑOL: cada texto del HTML lleva data-i18n="clave" (o data-i18n-alt / -aria-label / -content / -href
// para atributos) y su traducción está en el objeto ES. Para añadir un texto nuevo: pon la clave en el HTML y su
// traducción en ES. Comprueba que no falta nada con: python3 tools/comprobar-idiomas.py
(function () {
  var ES = {
    "ana_lopez_canellas_ux_ui_designer": "Ana López Canellas · Diseñadora UX/UI",
    "portfolio_of_ana_lopez_canellas_ux": "Portfolio de Ana López Canellas, diseñadora UX/UI: e-commerce, sanidad, accesibilidad y sistemas de diseño.",
    "skip_to_content": "Saltar al contenido",
    "main": "Principal",
    "projects": "Proyectos",
    "scroll_to_projects": "Ver proyectos",
    "about_me": "Sobre mí",
    "language": "Idioma",
    "dark_mode": "Modo oscuro",
    "ux_ui_designer": "Diseñadora UX/UI",
    "h1_a": "Diseño productos digitales para resolver problemas ",
    "h1_b": "reales",
    "h1_c": " de personas ",
    "h1_d": "reales",
    "h1_e": "",
    "i_work_in_e_commerce_healthcare": "Trabajo en e-commerce, sanidad, turismo y seguros, con foco en sistemas de diseño, accesibilidad y colaboración estrecha con desarrollo.",
    "for_confidentiality_reasons_clients_are_not": "Por confidencialidad, los clientes no se nombran: cada proyecto se presenta por sector y por el trabajo realizado.",
    "selected_work": "Trabajo seleccionado",
    "internal_project": "Proyecto interno",
    "internal_project_white_label_design_system": "Proyecto interno · Sistema de diseño de marca blanca",
    "internal": "Interno",
    "white_label_design_system": "Sistema de diseño de marca blanca",
    "white_label": "Marca blanca",
    "confidential_client": "Cliente confidencial",
    "information_architecture": "Arquitectura de información",
    "back_to_top": "Volver arriba",
    "about_me_ana_lopez_canellas": "Sobre mí · Ana López Canellas",
    "about_ana_lopez_canellas_ux_ui": "Sobre Ana López Canellas, diseñadora UX/UI: presentación, certificaciones y contacto.",
    "i_love_traveling": "Me gusta mucho viajar para conocer nuevas culturas y tratar de meterme lo máximo posible en el día a día del país al que voy. No me considero experta en fotografía, pero me apasiona capturar los lugares que visito, tanto en digital como en analógico.",
    "travel_photography": "Fotografía de viajes",
    "trip_01": "Entrada iluminada en rojo de un edificio con caracteres chinos y farolillos rojos contra un cielo azul intenso",
    "trip_02": "Un tramo de la Gran Muralla china serpenteando por una cresta de montaña verde",
    "trip_03": "Calle estrecha de casco antiguo con edificios altos de piedra y balcones",
    "trip_04": "Puestos de comida callejera con carteles chinos de colores, panes planos y helados",
    "trip_05": "Foto analógica de las cúpulas verdes de la catedral de Berlín con la torre de televisión detrás",
    "trip_06": "Foto analógica de un castillo de piedra en ruinas sobre un acantilado junto al mar, bajo un cielo brumoso",
    "trip_07": "Foto analógica del mural del Muro de Berlín con dos hombres besándose y grafitis debajo",
    "trip_08": "Foto analógica del perfil de una ciudad con bloques de viviendas y montañas al fondo",
    "trip_09": "Foto analógica de una gran puerta ceremonial blanca con tejados de tejas azules y arcos",
    "trip_10": "Foto analógica de una ciudad en una colina bañada por luz dorada sobre un río, con una bandera portuguesa en primer plano",
    "trip_11": "Foto analógica de barcos tradicionales de madera en un río frente a una ciudad de colores en la ladera",
    "trip_12": "Foto analógica del perfil de los rascacielos de una ciudad al atardecer, con nubes rosas sobre el agua",
    "trip_13": "Un eclipse solar total: un anillo brillante de luz en un cielo negro",
    "trip_14": "La torre de televisión de Berlín elevándose contra un cielo azul despejado",
    "trip_15": "Dos fotos instantáneas del cartel de bienvenida de Las Vegas sostenidas frente al cartel real",
    "trip_16": "La Space Needle de Seattle iluminada de noche, junto a un árbol de luces",
    "trip_17": "El cartel rojo de Public Market Center al atardecer sobre una multitud en Seattle",
    "trip_18": "Palmeras a contraluz contra un cielo naranja de atardecer entre edificios",
    "trip_19": "El Empire State Building visto desde la calle entre edificios altos y un cielo nublado",
    "trip_20": "El Parlamento de Hungría iluminado en dorado por la noche",
    "portrait_armchair": "Retrato en blanco y negro de Ana López Canellas sentada en un sillón, sonriendo con la cabeza ladeada",
    "portrait_great_wall": "Foto de Ana López Canellas sonriendo con gorra y conjunto deportivo morado, apoyada en una barandilla con la Gran Muralla china detrás",
    "my_passion_for_helping_others_led": "Mi pasión por ayudar a los demás me llevó al diseño de experiencia de usuario. Crear soluciones de diseño que mejoran la experiencia de las personas encaja a la perfección con mi deseo de tener un impacto real a través de mi trabajo.",
    "i_adapt_easily_to_different_circumstances": "Tengo una gran capacidad de adaptación a distintas circunstancias y afronto los retos con calma y de forma proactiva. Doy prioridad a un entorno sin estrés y practico una comunicación clara y asertiva para resolver los problemas de manera eficaz.",
    "design_systems_and_tokens": "Sistemas de diseño y tokens",
    "figma_variables_and_modes": "Figma: variables y modos",
    "accessibility_wcag": "Accesibilidad (WCAG)",
    "prototyping_and_user_flows": "Prototipado y flujos de usuario",
    "agile_methodologies": "Metodologías ágiles",
    "certifications": "Certificaciones",
    "home": "Inicio",
    "user_experience_ux_design": "Diseño de Experiencia del Usuario (UX)",
    "mobile_app_development_course": "Curso de Desarrollo de Apps Móviles",
    "spain": "España",
    "contact": "Contacto",
    "copy_to_clipboard": "(copiar al portapapeles)",
    "opens_in_a_new_tab": "(se abre en una pestaña nueva)",
    "internal_project_white_label_design_system_2": "Proyecto interno · Sistema de diseño de marca blanca · Ana López Canellas",
    "creation_of_a_white_label_design": "Creación de un sistema de diseño de marca blanca como base para proyectos futuros y propuestas rápidas a clientes, para que otros diseñadores no partan de ",
    "back_to_projects": "Volver a proyectos",
    "date": "Fecha",
    "company": "Empresa",
    "ai_with_claude_code": "IA con Claude Code",
    "design_system_color_palettes_scales_from": "Paletas de color del sistema de diseño: escalas de 100 a 950 del primario de marca, los grises neutros y los semánticos de error, éxito, aviso e información, cada tono con su ratio de contraste. Debajo, el panel de variables de Figma con las colecciones de color, tamaño, tipografía y movimiento.",
    "description": "Descripción",
    "creation_of_a_white_label_design_2": "Creación de un sistema de diseño de marca blanca como base para proyectos futuros y propuestas rápidas a clientes, para que otros diseñadores no partan de cero cuando llega un cliente sin sistema de diseño. Desarrollado casi por completo con inteligencia artificial (Claude Code).",
    "it_starts_from_a_base_with": "Parte de una base con los componentes básicos tanto de páginas web como de portales (AEM, LumApps, etc.), todos 100% configurables. Aparte, un archivo independiente reúne los componentes para el diseño de apps móviles, tanto en iOS como en Android.",
    "what_it_involved": "En qué consistió",
    "analysis_of_white_label_design_systems": "Análisis de sistemas de diseño de marca blanca.",
    "creation_of_a_complete_responsive_and": "Creación de un sistema completo, responsive y accesible.",
    "100_configurable_components_designed_for_the": "Componentes 100% configurables, pensados para web y para portales como AEM o LumApps.",
    "a_separate_file_with_the_mobile": "Archivo aparte con los componentes de diseño de apps móviles, para iOS y Android.",
    "exploration_of_claude_codes_limitations_and": "Exploración de las limitaciones de Claude Code y de los prompts adecuados para obtener el mejor resultado.",
    "refinement_of_the_components_once_generated": "Refinamiento de los componentes una vez generados por Claude.",
    "consistent_logical_variables_designed_to_be": "Variables consistentes y lógicas, pensadas para cambiarse con facilidad y reducir el tiempo de adaptación a cada proyecto.",
    "complete_documentation_of_the_system_in": "Documentación completa del sistema en archivos .md, lista para pasar al equipo de desarrollo.",
    "workshops_to_teach_other_designers_how": "Workshops para enseñar a otros diseñadores a usarlo.",
    "tools": "Herramientas",
    "structure": "Estructura",
    "the_system_is_split_across_three": "El sistema se reparte en tres archivos interconectados, cada uno con un propósito distinto.",
    "file_1_of_3": "Archivo 1 de 3",
    "the_master_reference_file_cover_templates": "El archivo maestro de referencia. Plantillas de portada, componentes de portada de flujos (principal, secundaria, variaciones y casos límite), marcos de anotaciones y diapositivas de los workshops, todo construido mediante la API de plugins de Figma.",
    "file_2_of_3": "Archivo 2 de 3",
    "a_fully_documented_component_library_for": "Una librería de componentes completamente documentada para el equipo de EMEA ATC. 17 componentes, cada uno con visión general, especificaciones, accesibilidad, propiedades y un marco con la descripción para desarrollo, todo generado por el agente de documentación.",
    "file_3_of_3": "Archivo 3 de 3",
    "designs_working_file": "Diseños (archivo de trabajo)",
    "where_the_real_product_flows_live": "Donde viven los flujos de producto reales. Contiene el flujo de referencia (registro, 12 pantallas) y su documentación completa con el sistema de portadas y anotaciones, usado como resultado de referencia durante el Workshop 2.",
    "ws_intro": "Dos workshops prácticos para que el equipo de EMEA ATC se inicie en flujos de trabajo en Figma asistidos por IA.",
    "ws_1_title": "Sesión 1 · Iniciar un proceso de trabajo",
    "ws_1_text": "Enseñamos a iniciar un proceso de trabajo con los archivos recién creados. Como el design system ya existía, el primer paso era duplicarlo y adaptar sus variables a los requisitos y a la marca del cliente. También vimos cómo conectar Claude Code al archivo de trabajo, para que pueda trabajar directamente sobre él y agilizar las tareas de diseño.",
    "ws_2_title": "Sesión 2 · Documentar flujos",
    "ws_2_text": "Después pasamos a flujos completos: cómo nombrar capas y marcos, cómo funciona el sistema de portadas y una rutina corta de cinco pasos de prompts para anotar un flujo. El grupo practicó con un flujo de registro, cada persona en su propia copia de los archivos.",
    "ws_aim": "La idea era que cada asistente se fuera con algo funcionando en su propio archivo de Figma, no solo con una idea de lo que es posible.",
    "workshops_image_alt": "Dos diseñadoras durante un workshop frente a una pantalla grande que muestra las variables de color del sistema de diseño en Figma",
    "applied_in_projects": "Aplicación en proyectos",
    "app_adaptation": "Adaptación a app",
    "web_and_mobile_app_3_screens": "Aplicación web y móvil · 3 pantallas",
    "web_adaptation": "Adaptación a web",
    "web_portal_4_screens": "Portal web · 4 pantallas",
    "close": "Cerrar",
    "the_design_system_applied_to_a": "Aplicación del sistema de diseño en una propuesta para cliente",
    "carousel": "carrusel",
    "previous_screen": "Pantalla anterior",
    "application_screen_slides": "Diapositivas de pantallas de aplicación",
    "1_of_3": "1 de 3",
    "slide": "diapositiva",
    "web_screen_of_a_client_proposal": "Pantalla web de una propuesta para cliente construida con el sistema de diseño: ficha de cliente con sus datos y un indicador de progreso a la izquierda, pestañas de navegación, un aviso de información pendiente y tres tarjetas de preguntas con etiquetas, opciones y botón de edición. Abajo, un botón de contorno y un botón principal.",
    "client_proposal_web_app_with_record": "Propuesta para cliente: aplicación web con ficha, pestañas, avisos y tarjetas",
    "2_of_3": "2 de 3",
    "web_screen_for_configuring_a_question": "Pantalla web de configuración de una pregunta en una propuesta para cliente: lista de preguntas con buscador a la izquierda, pestañas superiores, título con etiqueta de estado Activa, botón Nueva pregunta y secciones con reglas de cuándo y a quién se muestra, parametrización y botones de edición.",
    "client_proposal_configuration_screen_with_list": "Propuesta para cliente: pantalla de configuración con listado, buscador y formularios",
    "3_of_3": "3 de 3",
    "mobile_screen_of_a_client_proposal": "Pantalla móvil de una propuesta para cliente: cabecera con título, indicador de progreso por pasos con el paso 2 activo, la pregunta «¿La actividad de tu negocio requiere disponer de un local o establecimiento físico para desarrollarse?» con dos opciones de respuesta, la primera seleccionada, y abajo un botón de contorno «Pregunta anterior» y uno principal «Continuar».",
    "client_proposal_mobile_version_with_stepper": "Propuesta para cliente: versión móvil con stepper, opciones de respuesta y botones",
    "next_screen": "Pantalla siguiente",
    "the_design_system_applied_to_another": "Aplicación del sistema de diseño en otro proyecto",
    "previous_slide": "Diapositiva anterior",
    "web_adaptation_slides": "Diapositivas de la adaptación a web",
    "1_of_4": "1 de 4",
    "home_page_of_a_web_portal": "Página de inicio de un portal web con los componentes del sistema de diseño en los colores y redondeos de un cliente, con logotipos y textos desenfocados: cabecera negra con buscador y menú, carrusel destacado sobre fondo gris, una noticia con fecha y botón, una banda azul con un carrusel de tarjetas, un bloque Formación con cuatro tarjetas con icono y el pie de página.",
    "web_adaptation_portal_home_page_with": "Adaptación a web: página de inicio de un portal con carruseles, tarjetas y navegación",
    "2_of_4": "2 de 4",
    "listing_page_of_a_web_portal": "Página de listado de un portal web con los colores y redondeos de un cliente, con logotipos y textos desenfocados: cabecera negra con buscador y menú, migas de pan, un panel de filtros con campo de búsqueda y botones Cancelar y Aplicar, una tabla con cabecera azul ordenable por título y fecha de publicación, y paginación con la página 2 seleccionada.",
    "web_adaptation_listing_with_filters_sortable": "Adaptación a web: listado con filtros, tabla ordenable y paginación",
    "3_of_4": "3 de 4",
    "inner_page_of_a_web_portal": "Página interna de un portal web con los colores y redondeos de un cliente, con logotipos y textos desenfocados: cabecera negra con buscador y menú, migas de pan, un banner azul con una tarjeta blanca con el título «Sobre nosotros», un menú lateral de secciones con línea de selección y un contenido de texto con enlaces y listas, seguido de un pie de página negro con enlaces legales.",
    "web_adaptation_content_page_with_header": "Adaptación a web: página de contenido con cabecera, menú lateral y texto",
    "4_of_4": "4 de 4",
    "detail_page_of_a_web_portal": "Página de detalle de un portal web con los colores y redondeos de un cliente, con logotipos y textos desenfocados: cabecera negra con buscador y menú, migas de pan, un menú lateral con dos entradas, texto introductorio con enlace de contacto, una sección Material didáctico con tres tarjetas, un reproductor de vídeo negro con botón de reproducir, una sección Preguntas frecuentes con un listado de preguntas desplegables y el pie de página.",
    "web_adaptation_detail_page_with_learning": "Adaptación a web: página de detalle con material didáctico, vídeo y preguntas frecuentes",
    "next_slide": "Diapositiva siguiente",
    "more_projects": "Otros proyectos",
    "previous": "Anterior",
    "next": "Siguiente",
    "project_protected_by_a_confidentiality_agreement": "Proyecto protegido por acuerdo de confidencialidad",
    "get_in_touch_if_you_would": "Escríbeme si quieres saber más sobre él.",
    "email_me": "Escríbeme",
  "password_protected": "Protegido con contraseña",
  "gate_title": "Proyecto protegido",
  "gate_intro": "Este proyecto es confidencial. Introduce la contraseña que te he facilitado para verlo.",
  "gate_password": "Contraseña",
  "gate_view": "Ver proyecto",
  "gate_error": "Contraseña incorrecta. Inténtalo de nuevo.",
  "gate_nopw": "¿No tienes la contraseña?",
  "gate_ask": "Solicítame acceso"
  };

  // Traducciones de los proyectos generados con tools/construir.py (archivo autogenerado)
  var EXTRA = window.I18N_PROYECTOS || {};
  Object.keys(EXTRA).forEach(function (k) { ES[k] = EXTRA[k]; });

  // Textos que se usan desde JavaScript (main.js y unlock.js)
  var JS = {
    en: {
      copied: 'Email copied to clipboard',
      pauseCarousel: 'Pause travel photos',
      playCarousel: 'Play travel photos',
      copyFail: 'Could not copy; please type it manually: ',
      goSlide: 'Go to slide {0} of {1}',
      slide: 'Slide {0} of {1}',
      decrypting: 'Decrypting…',
      viewProject: 'View project',
      contents: 'Contents',
      filterTitle: 'Filter projects',
      fAll: 'All projects',
      fCompany: 'Company',
      fYear: 'Year',
      fSector: 'Client type',
      fShowing: 'Showing {0} of {1} projects',
      fNone: 'No projects match these filters.',
      noCrypto: 'Your browser cannot decrypt this content. Open the site over https in an up-to-date browser.'
    },
    es: {
      copied: 'Correo copiado al portapapeles',
      pauseCarousel: 'Pausar fotos de viajes',
      playCarousel: 'Reanudar fotos de viajes',
      copyFail: 'No se pudo copiar; escríbelo a mano: ',
      goSlide: 'Ir a la diapositiva {0} de {1}',
      slide: 'Diapositiva {0} de {1}',
      decrypting: 'Descifrando…',
      viewProject: 'Ver proyecto',
      contents: 'Contenidos',
      filterTitle: 'Filtrar proyectos',
      fAll: 'Todos los proyectos',
      fCompany: 'Empresa',
      fYear: 'Año',
      fSector: 'Tipo de cliente',
      fShowing: 'Mostrando {0} de {1} proyectos',
      fNone: 'Ningún proyecto coincide con estos filtros.',
      noCrypto: 'Tu navegador no permite descifrar este contenido. Abre la web con https en un navegador actualizado.'
    }
  };

  var DEFAULT = 'en';      // idioma si la persona no ha elegido y su navegador no está en español
  var STORE = 'lang';
  var ATTRS = ['alt', 'aria-label', 'aria-roledescription', 'title', 'content', 'href'];
  var SEL = '[data-i18n],' + ATTRS.map(function (a) { return '[data-i18n-' + a + ']'; }).join(',');
  var originales = new WeakMap();
  var actual = DEFAULT;

  function leer() {
    var p = /[?&]lang=(en|es)\b/.exec(location.search);
    if (p) return p[1];
    try { var s = localStorage.getItem(STORE); if (s === 'en' || s === 'es') return s; } catch (e) {}
    return /^es\b/i.test(navigator.language || '') ? 'es' : DEFAULT;
  }

  function traducir(el, lang) {
    var o = originales.get(el);
    if (!o) { o = { attrs: {} }; originales.set(el, o); }
    if (el.hasAttribute('data-i18n')) {
      if (o.text === undefined) o.text = el.textContent;
      var k = el.getAttribute('data-i18n');
      el.textContent = (lang === 'es' && ES[k] !== undefined) ? ES[k] : o.text;
    }
    ATTRS.forEach(function (a) {
      var kk = el.getAttribute('data-i18n-' + a);
      if (kk === null) return;
      if (o.attrs[a] === undefined) o.attrs[a] = el.getAttribute(a);
      el.setAttribute(a, (lang === 'es' && ES[kk] !== undefined) ? ES[kk] : o.attrs[a]);
    });
  }

  function aplicar(raiz, lang) {
    raiz = raiz || document;
    lang = lang || actual;
    if (raiz.matches && raiz.matches(SEL)) traducir(raiz, lang);
    raiz.querySelectorAll(SEL).forEach(function (el) { traducir(el, lang); });
  }

  function poner(lang, guardar) {
    actual = lang;
    document.documentElement.setAttribute('lang', lang);
    aplicar(document, lang);
    document.querySelectorAll('.lang-btn').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.getAttribute('data-lang') === lang));
    });
    if (guardar) { try { localStorage.setItem(STORE, lang); } catch (e) {} }
    window.dispatchEvent(new CustomEvent('alc:lang', { detail: lang }));
  }

  function t(clave) {
    var s = (JS[actual] && JS[actual][clave]) || JS.en[clave] || clave;
    for (var i = 1; i < arguments.length; i++) s = s.replace('{' + (i - 1) + '}', arguments[i]);
    return s;
  }

  window.i18n = { t: t, apply: aplicar, set: function (l) { poner(l, true); }, get: function () { return actual; } };

  document.querySelectorAll('.lang-btn').forEach(function (b) {
    b.addEventListener('click', function () { poner(b.getAttribute('data-lang'), true); });
  });
  poner(leer(), false);
})();
