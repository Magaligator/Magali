/* MAGALAÏ — interactions de la boutique (maquette, version blanche / noire) */
(function () {
  'use strict';
  document.documentElement.classList.add('js');
  var M = window.MAGALAI || { currency: 'CHF', freeShipping: 120, products: [] };
  var P = {};
  M.products.forEach(function (p) { P[p.slug] = p; });
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var body = document.body;
  var page = body.getAttribute('data-page');
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function fmt(n) {
    var v = Math.round(n * 100) / 100;
    return M.currency + ' ' + (v % 1 ? v.toFixed(2) : v);
  }
  var store = {
    get: function (k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var norm = function (s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };

  /* ───── toast ───── */
  var toastEl = $('.toast'), toastT;
  function toast(msg) {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add('show');
    clearTimeout(toastT);
    toastT = setTimeout(function () { toastEl.classList.remove('show'); }, 2600);
  }

  /* ───── en-tête ───── */
  var hdr = $('.site-header');
  function onScroll() { if (hdr) hdr.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ───── tiroirs & recherche ───── */
  var lastFocus = null;
  function openPanel(name) {
    lastFocus = document.activeElement;
    closePanels(true);
    body.classList.add('open-' + name);
    var el = $('#' + name);
    if (el) {
      el.setAttribute('aria-hidden', 'false');
      var t = name === 'search' ? $('#q') : $('[data-close]', el);
      setTimeout(function () { if (t) t.focus(); }, 80);
    }
    if (name === 'search') renderSearch('');
  }
  function closePanels(silent) {
    ['cart', 'menu', 'search'].forEach(function (n) {
      body.classList.remove('open-' + n);
      var el = $('#' + n);
      if (el) el.setAttribute('aria-hidden', 'true');
    });
    if (!silent && lastFocus && lastFocus.focus) lastFocus.focus();
  }
  document.addEventListener('click', function (e) {
    var o = e.target.closest('[data-open]');
    if (o) { e.preventDefault(); openPanel(o.getAttribute('data-open')); return; }
    if (e.target.closest('[data-close]')) { closePanels(); }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closePanels(); });

  function renderSearch(q) {
    var box = $('#results');
    if (!box) return;
    var n = norm(q).trim();
    var list = n ? M.products.filter(function (p) {
      return norm([p.name, p.label, p.typeLabel, p.collection, p.tagline].join(' ')).indexOf(n) > -1;
    }) : M.products.slice(0, 5);
    var head = n ? '' : '<p class="sr-hint">Suggestions</p>';
    if (!list.length) { box.innerHTML = '<p class="sr-hint">Aucun résultat pour « ' + q.replace(/[<>&]/g, '') + ' ». Essayez « créoles », « perles » ou un prénom.</p>'; return; }
    box.innerHTML = head + list.map(function (p) {
      return '<a class="sr-item" href="produit-' + p.slug + '.html"><img src="' + p.img + '" alt="" width="64" height="80"><div><strong>' + p.name + '</strong><span>' + p.label + ' · ' + p.collection + '</span></div><span>' + fmt(p.price) + '</span></a>';
    }).join('');
  }
  var qIn = $('#q');
  if (qIn) qIn.addEventListener('input', function () { renderSearch(qIn.value); });

  /* ───── favoris ───── */
  var favs = store.get('magalai_favs', []);
  function paintFavs() {
    $$('[data-fav]').forEach(function (b) {
      var on = favs.indexOf(b.getAttribute('data-fav')) > -1;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    setCount('[data-fav-count]', favs.length);
  }
  function setCount(sel, n) {
    $$(sel).forEach(function (c) {
      var changed = c.textContent !== String(n);
      c.textContent = n; c.setAttribute('data-n', n);
      if (changed) { c.classList.add('bump'); setTimeout(function () { c.classList.remove('bump'); }, 300); }
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('[data-fav]');
    if (!b) return;
    var s = b.getAttribute('data-fav'), i = favs.indexOf(s);
    if (i > -1) favs.splice(i, 1); else { favs.push(s); toast(P[s].name + ' ajoutée à vos favoris'); }
    store.set('magalai_favs', favs);
    paintFavs();
    if (page === 'boutique' && shop && shop.state.filter === 'favoris') shop.apply();
  });

  /* ───── panier ───── */
  var cart = store.get('magalai_cart', []);
  function saveCart() { store.set('magalai_cart', cart); renderCart(); }
  function subtotal() { return cart.reduce(function (t, l) { return t + (P[l.slug] ? P[l.slug].price * l.qty : 0); }, 0); }
  function addToCart(slug, qty, gift) {
    if (!P[slug]) return;
    var l = cart.filter(function (x) { return x.slug === slug; })[0];
    if (l) { l.qty += qty; if (gift) l.gift = true; } else cart.push({ slug: slug, qty: qty, gift: !!gift });
    saveCart();
  }
  function renderCart() {
    var n = cart.reduce(function (t, l) { return t + l.qty; }, 0);
    setCount('[data-cart-count]', n);
    var wrap = $('[data-cart-items]');
    if (!wrap) return;
    var sub = subtotal();
    if (!cart.length) {
      wrap.innerHTML = '<div class="cart-empty"><h3>Votre panier est vide</h3><p>Chaque paire attend de raconter son histoire.</p><a class="btn btn-dark" href="boutique.html">Découvrir la boutique</a></div>';
      $('[data-cart-foot]').style.display = 'none';
    } else {
      $('[data-cart-foot]').style.display = '';
      wrap.innerHTML = cart.map(function (l) {
        var p = P[l.slug];
        return '<div class="cart-line" data-line="' + l.slug + '"><a href="produit-' + p.slug + '.html"><img src="' + p.img + '" alt="" width="88" height="110"></a><div><h3>' + p.name + '</h3><p class="m">' + p.label + (l.gift ? ' · écrin cadeau' : '') + '</p><div class="qty"><button type="button" data-cq="-1" aria-label="Moins"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 12h14"/></svg></button><output>' + l.qty + '</output><button type="button" data-cq="1" aria-label="Plus"><svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 5v14M5 12h14"/></svg></button></div><button class="rm" type="button" data-rm>Retirer</button></div><div class="p">' + fmt(p.price * l.qty) + '</div></div>';
      }).join('');
    }
    var st = $('[data-cart-subtotal]'); if (st) st.textContent = fmt(sub);
    var msg = $('[data-ship-msg]'), fill = $('[data-ship-fill]');
    if (msg) {
      var left = M.freeShipping - sub;
      msg.innerHTML = !cart.length ? 'Livraison offerte dès <strong>' + fmt(M.freeShipping) + '</strong>'
        : left > 0 ? 'Plus que <strong>' + fmt(left) + '</strong> pour la livraison offerte'
        : 'Votre livraison est <strong>offerte</strong> ✦';
      fill.style.width = Math.min(100, (sub / M.freeShipping) * 100) + '%';
    }
    if (page === 'commande') renderCheckout();
  }
  document.addEventListener('click', function (e) {
    var add = e.target.closest('[data-add]');
    if (add) {
      e.preventDefault();
      var slug = add.getAttribute('data-add');
      var from = add.getAttribute('data-qty-from');
      var qty = from ? parseInt($(from).textContent, 10) || 1 : 1;
      var g = $('#gift-chk');
      addToCart(slug, qty, g && g.checked);
      openPanel('cart');
      return;
    }
    var line = e.target.closest('[data-line]');
    if (!line) return;
    var slug2 = line.getAttribute('data-line');
    var l = cart.filter(function (x) { return x.slug === slug2; })[0];
    var cq = e.target.closest('[data-cq]');
    if (cq && l) { l.qty += parseInt(cq.getAttribute('data-cq'), 10); if (l.qty < 1) cart = cart.filter(function (x) { return x !== l; }); saveCart(); }
    if (e.target.closest('[data-rm]')) { cart = cart.filter(function (x) { return x.slug !== slug2; }); saveCart(); }
  });

  /* ───── révélations au scroll ───── */
  var revealEls = $$('.reveal, .img-reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
    }, { threshold: .12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else { revealEls.forEach(function (el) { el.classList.add('in'); }); }

  /* ───── sélecteur d'humeur ───── */
  $$('[data-mood]').forEach(function (b) {
    b.addEventListener('click', function () {
      var m = b.getAttribute('data-mood');
      $$('[data-mood]').forEach(function (x) { var on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-pressed', on); });
      $$('[data-res]').forEach(function (r) { r.classList.toggle('on', r.getAttribute('data-res') === m); });
    });
  });

  /* ───── newsletter & contact ───── */
  $$('[data-newsletter]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      f.innerHTML = '<p style="grid-column:1/-1;color:inherit;font-size:1.05rem;padding:14px 0">Merci ✦ Votre code <strong>MAGALAI10</strong> arrive par e-mail.</p>';
      toast('Bienvenue — code MAGALAI10 : −10 %');
    });
  });
  var cf = $('[data-contact]');
  if (cf) cf.addEventListener('submit', function (e) { e.preventDefault(); $('.form-ok', cf).hidden = false; cf.reset(); });

  /* ───── rails : glisser à la souris ───── */
  $$('[data-rail]').forEach(function (rail) {
    var down = false, sx = 0, sl = 0, moved = 0;
    rail.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse') return;
      down = true; moved = 0; sx = e.clientX; sl = rail.scrollLeft; rail.classList.add('drag');
    });
    window.addEventListener('pointermove', function (e) {
      if (!down) return;
      var dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx));
      rail.scrollLeft = sl - dx;
    });
    window.addEventListener('pointerup', function () { if (down) { down = false; rail.classList.remove('drag'); } });
    rail.addEventListener('click', function (e) { if (moved > 6) { e.preventDefault(); e.stopPropagation(); moved = 0; } }, true);
  });

  /* ───── curseur personnalisé ───── */
  (function () {
    var cur = $('.cursor');
    if (!cur || !window.matchMedia('(hover:hover) and (pointer:fine)').matches || reduceMotion) return;
    var dot = $('i', cur), ring = $('span', cur);
    var x = -100, y = -100, rx = -100, ry = -100, started = false;
    document.addEventListener('mousemove', function (e) {
      x = e.clientX; y = e.clientY;
      if (!started) { started = true; rx = x; ry = y; cur.classList.add('on'); loop(); }
      dot.style.translate = x + 'px ' + y + 'px';
      var t = e.target;
      var view = t.closest && t.closest('.card-media, .tile, .panel, .coll-media, .g-item, .card-edito, .quiz-img, .comm-grid a');
      var hov = t.closest && t.closest('a, button, input, select, summary, label, .chip');
      cur.classList.toggle('view', !!view);
      cur.classList.toggle('hover', !!hov && !view);
    }, { passive: true });
    document.addEventListener('mouseleave', function () { cur.classList.remove('on'); });
    document.addEventListener('mouseenter', function () { if (started) cur.classList.add('on'); });
    function loop() {
      rx += (x - rx) * .18; ry += (y - ry) * .18;
      ring.style.translate = rx + 'px ' + ry + 'px';
      requestAnimationFrame(loop);
    }
  })();

  /* ───── boutique : filtres ───── */
  var shop = null;
  if (page === 'boutique') {
    var grid = $('#shop-grid');
    var cards = $$('.card', grid);
    var edito = $('[data-edito]', grid);
    var order = cards.slice();
    var qs = new URLSearchParams(location.search);
    var st = { type: qs.get('type') || 'all', col: qs.get('collection') || 'all', price: 'all', sort: 'featured', filter: qs.get('filter') || '' };
    var colMap = {}; M.products.forEach(function (p) { colMap[norm(p.collection)] = p.collection; });
    var typeLabels = {}; M.products.forEach(function (p) { typeLabels[p.type] = p.typeLabel; });
    var chips = $$('[data-type]');
    var selCol = $('#f-col'), selPrice = $('#f-price'), selSort = $('#f-sort');
    selCol.value = st.col; if (selCol.value !== st.col) { st.col = 'all'; selCol.value = 'all'; }
    function apply() {
      var pr = st.price === 'all' ? null : st.price.split('-').map(Number);
      var vis = cards.filter(function (c) {
        var d = c.dataset, ok = true;
        if (st.type !== 'all' && d.type !== st.type) ok = false;
        if (st.col !== 'all' && d.collection !== st.col) ok = false;
        if (pr && (+d.price < pr[0] || +d.price >= pr[1])) ok = false;
        if (st.filter === 'nouveau' && d.new !== '1') ok = false;
        if (st.filter === 'best' && d.best !== '1') ok = false;
        if (st.filter === 'favoris' && favs.indexOf(d.slug) < 0) ok = false;
        c.hidden = !ok;
        return ok;
      });
      var sorted = order.slice();
      if (st.sort === 'asc') sorted.sort(function (a, b) { return a.dataset.price - b.dataset.price; });
      if (st.sort === 'desc') sorted.sort(function (a, b) { return b.dataset.price - a.dataset.price; });
      if (st.sort === 'az') sorted.sort(function (a, b) { return a.dataset.name.localeCompare(b.dataset.name, 'fr'); });
      if (st.sort === 'new') sorted.sort(function (a, b) { return b.dataset.new - a.dataset.new; });
      sorted.forEach(function (c) { grid.appendChild(c); });
      var plain = st.type === 'all' && st.col === 'all' && st.price === 'all' && !st.filter && st.sort === 'featured';
      if (edito) {
        edito.hidden = !plain;
        if (plain) grid.insertBefore(edito, sorted[6] || null);
      }
      $('[data-count]').textContent = vis.length + (vis.length > 1 ? ' modèles' : ' modèle');
      $('#empty').hidden = vis.length > 0;
      grid.hidden = vis.length === 0;
      var em = $('[data-empty-msg]');
      if (em) em.textContent = st.filter === 'favoris' && !favs.length ? 'Cliquez sur le cœur d\'une boucle pour la retrouver ici.' : 'Essayez d\'autres filtres, ou découvrez l\'ensemble de la boutique.';
      chips.forEach(function (c) { c.classList.toggle('on', c.getAttribute('data-type') === st.type); });
      var t = $('[data-shop-title]');
      if (st.filter === 'nouveau') t.innerHTML = 'Les <em>nouveautés</em>';
      else if (st.filter === 'favoris') t.innerHTML = 'Mes <em>favoris</em>';
      else if (st.col !== 'all') t.innerHTML = 'Collection <em>' + (colMap[st.col] || st.col) + '</em>';
      else if (st.type !== 'all') t.innerHTML = '<em>' + typeLabels[st.type] + '</em>';
      else t.innerHTML = 'Toutes les <em>boucles d\'oreilles</em>';
    }
    chips.forEach(function (c) { c.addEventListener('click', function () { st.type = c.getAttribute('data-type'); apply(); }); });
    selCol.addEventListener('change', function () { st.col = selCol.value; apply(); });
    selPrice.addEventListener('change', function () { st.price = selPrice.value; apply(); });
    selSort.addEventListener('change', function () { st.sort = selSort.value; apply(); });
    $$('[data-cols]').forEach(function (b) {
      b.addEventListener('click', function () {
        var n = b.getAttribute('data-cols');
        grid.classList.toggle('g3', n === '3'); grid.classList.toggle('g4', n === '4');
        $$('[data-cols]').forEach(function (x) { x.classList.toggle('on', x === b); });
      });
    });
    shop = { state: st, apply: apply };
    apply();
  }

  /* ───── fiche produit ───── */
  if (page === 'produit') {
    var qn = $('#qty');
    $$('[data-q]').forEach(function (b) {
      b.addEventListener('click', function () {
        qn.textContent = Math.max(1, Math.min(10, (parseInt(qn.textContent, 10) || 1) + parseInt(b.getAttribute('data-q'), 10)));
      });
    });
    var buy = $('.buy'), sticky = $('.sticky-atc');
    if (buy && sticky && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (en) {
        var e = en[0];
        sticky.classList.toggle('show', !e.isIntersecting && e.boundingClientRect.top < 0);
      }).observe(buy);
    }
    // points de la galerie (mobile)
    var gal = $('.gallery'), dots = $$('.g-dots i');
    if (gal && dots.length) {
      gal.addEventListener('scroll', function () {
        var it = $('.g-item', gal); if (!it) return;
        var step = it.getBoundingClientRect().width + 8;
        var i = Math.max(0, Math.min(dots.length - 1, Math.round(gal.scrollLeft / step)));
        dots.forEach(function (d, k) { d.classList.toggle('on', k === i); });
      }, { passive: true });
    }
    // livraison estimée
    var dl = $('[data-delivery]');
    if (dl) {
      var addDays = function (n) { var d = new Date(), k = 0; while (k < n) { d.setDate(d.getDate() + 1); if (d.getDay() % 6) k++; } return d; };
      var f = function (d) { return d.toLocaleDateString('fr-CH', { weekday: 'short', day: 'numeric', month: 'short' }); };
      dl.textContent = 'Livraison estimée entre le ' + f(addDays(2)) + ' et le ' + f(addDays(4));
    }
    // lightbox
    var lb = $('#lb'), items = $$('.g-item'), li = 0;
    if (lb) {
      var lbImg = $('img', lb);
      var show = function (i) { li = (i + items.length) % items.length; lbImg.src = items[li].getAttribute('data-zoom'); };
      var closeLb = function () { lb.hidden = true; body.style.overflow = ''; };
      items.forEach(function (it, i) { it.addEventListener('click', function () { show(i); lb.hidden = false; body.style.overflow = 'hidden'; }); });
      $('.lb-close', lb).addEventListener('click', closeLb);
      $('.lb-prev', lb).addEventListener('click', function () { show(li - 1); });
      $('.lb-next', lb).addEventListener('click', function () { show(li + 1); });
      lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
      document.addEventListener('keydown', function (e) {
        if (lb.hidden) return;
        if (e.key === 'Escape') closeLb();
        if (e.key === 'ArrowLeft') show(li - 1);
        if (e.key === 'ArrowRight') show(li + 1);
      });
    }
  }

  /* ───── commande ───── */
  var promoOn = false;
  function renderCheckout() {
    var form = $('#checkout'), sum = $('.co-sum'), empty = $('.co-empty');
    if (!form) return;
    if (!cart.length && !body.classList.contains('done')) {
      form.hidden = true; sum.hidden = true; empty.hidden = false; return;
    }
    $('[data-co-items]').innerHTML = cart.map(function (l) {
      var p = P[l.slug];
      return '<div class="sum-line"><img src="' + p.img + '" alt="" width="64" height="80"><div><strong>' + p.name + '</strong><span>' + p.label + ' × ' + l.qty + '</span></div><span>' + fmt(p.price * l.qty) + '</span></div>';
    }).join('');
    var sub = subtotal(), disc = promoOn ? sub * 0.1 : 0;
    var ex = form.elements.ship.value === 'exp';
    var ship = ex ? 15 : (sub - disc >= M.freeShipping ? 0 : 6.9);
    $('[data-co-sub]').textContent = fmt(sub);
    $('.disc').hidden = !promoOn;
    $('[data-co-disc]').textContent = '− ' + fmt(disc);
    $('[data-co-ship]').textContent = ship === 0 ? 'Offerte' : fmt(ship);
    $('[data-co-total]').textContent = fmt(sub - disc + ship);
    var std = $('[data-ship-std]'); if (std) std.textContent = (sub - disc >= M.freeShipping) ? 'Offerte' : 'CHF 6.90';
  }
  if (page === 'commande') {
    var form = $('#checkout');
    $$('input[name=ship]').forEach(function (r) { r.addEventListener('change', renderCheckout); });
    $('#promo-btn').addEventListener('click', function () {
      var v = $('#promo').value.trim().toUpperCase();
      promoOn = v === 'MAGALAI10';
      toast(promoOn ? 'Code appliqué : −10 %' : 'Code non valide');
      renderCheckout();
    });
    $$('input[name=pay]').forEach(function (r) {
      r.addEventListener('change', function () { $('.card-fields').style.display = r.value === 'card' ? '' : 'none'; });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      body.classList.add('done');
      $('[data-done-name]').textContent = form.elements.prenom.value;
      $('[data-done-ref]').textContent = '#MAG-' + Math.floor(10000 + Math.random() * 89999);
      cart = []; store.set('magalai_cart', cart);
      form.hidden = true; $('.co-sum').hidden = true; $('.co-done').hidden = false;
      renderCart();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ════════════ HERO : slider WebGL (transition liquide) ════════════ */
  var VS = 'attribute vec2 p;varying vec2 v;void main(){v=p*.5+.5;gl_Position=vec4(p,0.,1.);}';
  var FS = [
    '#ifdef GL_FRAGMENT_PRECISION_HIGH', 'precision highp float;', '#else', 'precision mediump float;', '#endif',
    'varying vec2 v;uniform sampler2D ta,tb;uniform vec2 res,sa,sb,fa,fb,mouse;uniform float prog,time,za,zb;',
    'float h(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}',
    'float n(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(h(i),h(i+vec2(1.,0.)),f.x),mix(h(i+vec2(0.,1.)),h(i+vec2(1.,1.)),f.x),f.y);}',
    'float fbm(vec2 p){float a=.5,s=0.;for(int i=0;i<4;i++){s+=a*n(p);p*=2.03;a*=.5;}return s;}',
    'vec2 cover(vec2 uv,vec2 img,vec2 foc,float z){float ra=res.x/res.y,ri=img.x/img.y;vec2 sc=ra>ri?vec2(1.,ri/ra):vec2(ra/ri,1.);sc/=z;vec2 off=clamp(foc-.5*sc,vec2(0.),vec2(1.)-sc);return off+uv*sc;}',
    'void main(){',
    ' vec2 uv=v;',
    ' float t=time*.00005;',
    ' float nz=fbm(uv*vec2(3.,2.2)+t*40.);',
    ' float d=uv.y*.75+uv.x*.25;',
    ' float edge=d+(nz-.5)*.55;',
    ' float soft=.22;',
    ' float thr=prog*(1.+soft)-soft*.5;',
    ' float m=smoothstep(thr-soft*.5,thr+soft*.5,edge);',
    ' float bump=sin(prog*3.14159);',
    ' vec2 disp=vec2(nz-.5,fbm(uv*3.+7.)-.5)*.16*bump;',
    ' vec2 par=(mouse-.5)*.018;',
    ' vec2 sp=vec2(.012,.004)*bump;',
    ' vec3 c=vec3(0.);',
    ' for(int k=0;k<3;k++){',
    '  float sg=float(k)-1.;',
    '  vec2 u=uv+disp*m+sp*sg;',
    '  vec3 A=texture2D(ta,cover(u+par,sa,fa,za)).rgb;',
    '  vec3 B=texture2D(tb,cover(u+par*1.4-disp*(1.-m),sb,fb,zb)).rgb;',
    '  vec3 mx=mix(B,A,m);',
    '  if(k==0)c.r=mx.r;else if(k==1)c.g=mx.g;else c.b=mx.b;',
    ' }',
    ' float seam=smoothstep(.05,0.,abs(edge-thr))*bump;',
    ' c+=seam*.32;',
    ' float vg=smoothstep(1.2,.3,length(uv-.5)*1.2);',
    ' c*=.88+.12*vg;',
    ' gl_FragColor=vec4(c,1.);',
    '}'
  ].join('\n');

  function initGL(canvas, stage, slides) {
    var urls = window.MAGALAI_HERO;
    if (!urls || !urls.length) throw new Error('no data');
    var gl = canvas.getContext('webgl', { antialias: false, alpha: false }) || canvas.getContext('experimental-webgl');
    if (!gl) throw new Error('no webgl');
    function sh(type, src) {
      var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
      return s;
    }
    var pr = gl.createProgram();
    gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS));
    gl.linkProgram(pr);
    if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) throw new Error('link');
    gl.useProgram(pr);
    var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
    var U = {}; ['ta', 'tb', 'res', 'sa', 'sb', 'fa', 'fb', 'mouse', 'prog', 'time', 'za', 'zb'].forEach(function (k) { U[k] = gl.getUniformLocation(pr, k); });
    gl.uniform1i(U.ta, 0); gl.uniform1i(U.tb, 1);

    var tex = [], loaded = 0, firstReady = false;
    urls.forEach(function (u, i) {
      var img = new Image();
      img.onload = function () {
        var t = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D, t);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        tex[i] = { t: t, w: img.naturalWidth, h: img.naturalHeight };
        loaded++;
        if (i === 0 && !firstReady) { firstReady = true; stage.classList.add('gl'); size(); draw(performance.now()); }
      };
      img.src = u;
    });

    var a = 0, b = 0, prog = 0, anim = null, mouse = [.5, .5], mt = [.5, .5], visible = true, raf = 0;
    function size() {
      var dpr = Math.min(window.devicePixelRatio || 1, 1.75);
      var w = Math.max(2, Math.round(stage.clientWidth * dpr)), hh = Math.max(2, Math.round(stage.clientHeight * dpr));
      if (canvas.width !== w || canvas.height !== hh) { canvas.width = w; canvas.height = hh; }
      gl.viewport(0, 0, canvas.width, canvas.height);
    }
    window.addEventListener('resize', function () { size(); draw(performance.now()); });
    stage.addEventListener('pointermove', function (e) {
      var r = stage.getBoundingClientRect();
      mt = [(e.clientX - r.left) / r.width, 1 - (e.clientY - r.top) / r.height];
      var x = $('[data-x]'), y = $('[data-y]');
      if (x) x.textContent = mt[0].toFixed(2); if (y) y.textContent = (1 - mt[1]).toFixed(2);
    });
    function ease(x) { return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
    function draw(now) {
      var A = tex[a], B = tex[b];
      if (!A) return;
      if (!B) B = A;
      mouse[0] += (mt[0] - mouse[0]) * .06; mouse[1] += (mt[1] - mouse[1]) * .06;
      if (anim) {
        var k = Math.min(1, (now - anim.t0) / anim.dur);
        prog = ease(k);
        if (k >= 1) { a = b; prog = 0; var cb = anim.cb; anim = null; if (cb) cb(); A = tex[a]; B = A; }
      }
      var fa = slides[a], fb = slides[b];
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, A.t);
      gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, B.t);
      gl.uniform2f(U.res, canvas.width, canvas.height);
      gl.uniform2f(U.sa, A.w, A.h); gl.uniform2f(U.sb, B.w, B.h);
      gl.uniform2f(U.fa, fa.fx, 1 - fa.fy); gl.uniform2f(U.fb, fb.fx, 1 - fb.fy);
      gl.uniform2f(U.mouse, mouse[0], mouse[1]);
      gl.uniform1f(U.prog, prog); gl.uniform1f(U.time, now);
      var breathe = 1.04 + .025 * Math.sin(now * .0004);
      gl.uniform1f(U.za, breathe + .1 * prog);
      gl.uniform1f(U.zb, breathe + .16 * (1 - prog));
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    function loop(now) { if (visible && !document.hidden) draw(now); raf = requestAnimationFrame(loop); }
    raf = requestAnimationFrame(loop);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (en) { visible = en[0].isIntersecting; }).observe(stage);
    return {
      to: function (i, cb) {
        if (!tex[i]) { a = b = i; if (cb) cb(); return; }
        b = i;
        if (reduceMotion) { a = i; prog = 0; if (cb) cb(); return; }
        anim = { t0: performance.now(), dur: 1500, cb: cb };
      }
    };
  }

  function initHero() {
    var root = $('[data-hero]');
    if (!root) return;
    var slides = JSON.parse(root.getAttribute('data-slides'));
    var stage = $('[data-stage]', root), canvas = $('#gl', root);
    var E = {
      n: $('[data-hero-n]', root), coll: $('[data-hero-coll]', root), name: $('[data-hero-name]', root), tag: $('[data-hero-tag]', root),
      desc: $('[data-hero-desc]', root), price: $('[data-hero-price]', root), link: $('[data-hero-link]', root),
      idx: $('[data-hero-idx]', root), fig: $('[data-hero-fig]', root)
    };
    var ticks = $$('.tick', root), fbs = $$('.hero-fb', root);
    var DUR = 7000, cur = 0, busy = false, timer = null, inView = true, api = null;
    try { api = initGL(canvas, stage, slides); } catch (e) { api = null; if (window.console) console.warn('[magalai] WebGL indisponible, slider CSS utilisé :', e && e.message); }

    function setText(i) {
      var s = slides[i];
      E.name.innerHTML = '<span class="swap">' + s.name + '</span>';
      E.n.textContent = 'N°' + s.n; E.coll.textContent = 'Collection ' + s.coll;
      E.tag.textContent = s.tag; E.desc.textContent = s.desc; E.price.textContent = s.price;
      E.link.setAttribute('href', s.href);
      E.idx.textContent = ('0' + (i + 1)).slice(-2); E.fig.textContent = ('0' + (i + 1)).slice(-2);
    }
    function paintTicks(i) {
      ticks.forEach(function (t, k) { t.classList.remove('on', 'done'); if (k < i) t.classList.add('done'); });
      var t = ticks[i];
      t.style.setProperty('--dur', DUR + 'ms');
      void t.offsetWidth;
      t.classList.add('on');
    }
    function schedule() {
      clearTimeout(timer);
      if (reduceMotion || !inView || document.hidden) return;
      timer = setTimeout(function () { go(cur + 1); }, DUR);
    }
    function go(i) {
      i = (i + slides.length) % slides.length;
      if (i === cur || busy) return;
      cur = i; busy = true;
      setText(i); paintTicks(i);
      fbs.forEach(function (f, k) { f.classList.toggle('on', k === i); });
      if (api) api.to(i, function () { busy = false; }); else setTimeout(function () { busy = false; }, 600);
      schedule();
    }
    $('[data-next]', root).addEventListener('click', function () { go(cur + 1); });
    $('[data-prev]', root).addEventListener('click', function () { go(cur - 1); });
    ticks.forEach(function (t) { t.addEventListener('click', function () { go(parseInt(t.getAttribute('data-go'), 10)); }); });
    document.addEventListener('keydown', function (e) {
      if (!inView || /input|textarea|select/i.test((e.target.tagName || ''))) return;
      if (e.key === 'ArrowRight') go(cur + 1);
      if (e.key === 'ArrowLeft') go(cur - 1);
    });
    var sx = null;
    stage.addEventListener('pointerdown', function (e) { sx = e.clientX; });
    window.addEventListener('pointerup', function (e) {
      if (sx == null) return;
      var dx = e.clientX - sx; sx = null;
      if (Math.abs(dx) > 50) go(cur + (dx < 0 ? 1 : -1));
    });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) {
        inView = en[0].isIntersecting;
        root.classList.toggle('paused', !inView);
        if (inView) { paintTicks(cur); schedule(); } else clearTimeout(timer);
      }, { threshold: .25 }).observe(root);
    }
    document.addEventListener('visibilitychange', function () { if (document.hidden) clearTimeout(timer); else { paintTicks(cur); schedule(); } });
    setText(0); paintTicks(0); schedule();
  }
  initHero();

  paintFavs();
  renderCart();
})();
