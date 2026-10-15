# -*- coding: utf-8 -*-
"""Génère le site MAGALAÏ — version blanche / noire (maquette e-commerce).
Usage : python3 build.py
Photos produits : assets/img/produits/<prenom>-1/2/3.(jpg|png|webp) — dépose les tiennes (jpg prioritaire) puis relance.
Photos de référence : voir assets/img/SOURCES.txt (à remplacer avant mise en ligne).
"""
import os, json, html
from data import *

ROOT = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(ROOT, "assets", "img", "produits")
SITE_URL = "https://magaligator.github.io/Magali"   # à changer le jour où tu as un nom de domaine (ex. https://www.magalai.ch) puis relancer build.py
CUR = "index.html"   # page en cours de génération (pour canonical / sitemap)
TODAY = __import__("datetime").date.today().isoformat()

BY_SLUG = {p["slug"]: p for p in PRODUCTS}
TYPE_LABEL = dict(TYPES)
NUM = {p["slug"]: i + 1 for i, p in enumerate(PRODUCTS)}
FRAGILE = {"aaliyah": "perles", "ines": "perles", "naima": "strass", "amara": "cristaux"}


def w(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def price(p):
    return f"{CURRENCY} {p}"


def esc(s):
    return html.escape(s, quote=True)


def real_image(base):
    for ext in ("jpg", "jpeg", "png", "webp"):
        if os.path.exists(os.path.join(PROD, f"{base}.{ext}")):
            return f"assets/img/produits/{base}.{ext}"
    return None


def pimg(p, n):
    return real_image(f"{p['slug']}-{n}") or f"assets/img/produits/{p['slug']}-{n}.webp"


def alt_for(p, n):
    views = {1: "vue produit", 2: "portée", 3: "ambiance"}
    return f"Boucles d'oreilles {p['name']} — {p['label']}, {views[n]}"


def photo(name):
    for ext in ("jpg", "png", "webp"):
        if os.path.exists(os.path.join(ROOT, "assets", "img", "photos", f"{name}.{ext}")):
            return f"assets/img/photos/{name}.{ext}"
    return f"assets/img/photos/{name}.webp"


def n2(i):
    return f"{i:02d}"


# ───────────────────────── icônes ─────────────────────────
def ic(name, cls="ic"):
    paths = {
        "heart": '<path d="M12 20.5s-7.5-4.6-9.3-9.2C1.4 7.9 3.6 5 6.7 5c2 0 3.5 1.1 5.3 3.2C13.8 6.1 15.3 5 17.3 5c3.1 0 5.3 2.9 4 6.3-1.8 4.6-9.3 9.2-9.3 9.2z"/>',
        "bag": '<path d="M5 8h14l-1 12H6L5 8z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
        "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
        "menu": '<path d="M4 8h16M4 16h16"/>',
        "close": '<path d="M6 6l12 12M18 6L6 18"/>',
        "arrow": '<path d="M4 12h15M13 6l6 6-6 6"/>',
        "arrow-l": '<path d="M20 12H5M11 6l-6 6 6 6"/>',
        "plus": '<path d="M12 5v14M5 12h14"/>',
        "minus": '<path d="M5 12h14"/>',
        "truck": '<path d="M2.5 6.5h11v9h-11zM13.5 10h4l3 3v2.5h-7z"/><circle cx="7" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/>',
        "return": '<path d="M4 9h11a5 5 0 0 1 0 10H8"/><path d="M8 5L4 9l4 4"/>',
        "gift": '<rect x="3.5" y="9" width="17" height="11" rx="1"/><path d="M12 9v11M3.5 13.5h17"/><path d="M12 9C9 9 7.5 7.5 8 6.2c.6-1.4 3-.9 4 2.8 1-3.7 3.4-4.2 4-2.8.5 1.3-1 2.8-4 2.8z"/>',
        "lock": '<rect x="5" y="10.5" width="14" height="9.5" rx="1.5"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/>',
        "gem": '<path d="M6 4h12l3.5 5L12 20.5 2.5 9 6 4z"/><path d="M2.5 9h19M9 4l-1.5 5L12 20.5M15 4l1.5 5L12 20.5"/>',
        "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
        "drop": '<path d="M12 3.5s-6 6.3-6 10.6a6 6 0 0 0 12 0C18 9.8 12 3.5 12 3.5z"/>',
        "shield": '<path d="M12 3l7.5 3v5.5c0 4.5-3 8-7.5 9.5-4.5-1.5-7.5-5-7.5-9.5V6z"/><path d="M8.8 12l2.2 2.2 4.2-4.4"/>',
        "layers": '<path d="M12 3.5l9 4.5-9 4.5L3 8z"/><path d="M3 12.5l9 4.5 9-4.5"/><path d="M3 16.5l9 4.5 9-4.5"/>',
        "ring": '<circle cx="12" cy="12" r="7.5"/><circle cx="12" cy="12" r="3.2"/>',
        "spark": '<path d="M12 3l1.8 6.2L20 11l-6.2 1.8L12 19l-1.8-6.2L4 11l6.2-1.8z"/>',
        "leaf": '<path d="M5 19c0-8 5-13 14-14 0 9-5 14-13 14"/><path d="M5 19l8-8"/>',
        "grid4": '<path d="M4 4h4v4H4zM10 4h4v4h-4zM16 4h4v4h-4zM4 10h4v4H4zM10 10h4v4h-4zM16 10h4v4h-4zM4 16h4v4H4zM10 16h4v4h-4zM16 16h4v4h-4z"/>',
        "grid2": '<path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"/>',
    }
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[name]}</svg>')


# ───────────────────────── composants ─────────────────────────
def card(p, lazy=True):
    badge = f'<span class="badge">{p["badge"]}</span>' if p["badge"] else ""
    ld = ' loading="lazy"' if lazy else ""
    return f'''<article class="card" data-slug="{p['slug']}" data-name="{esc(p['name'])}" data-type="{p['type']}" data-collection="{p['collection']}" data-price="{p['price']}" data-new="{1 if p['badge']=='Nouveau' else 0}" data-best="{1 if p['badge']=='Best-seller' else 0}">
  <div class="card-top">
    <a class="card-media" href="produit-{p['slug']}.html" aria-label="{esc(p['name'])} — {esc(p['label'])}">
      <img class="m1" src="{pimg(p,1)}" alt="{esc(alt_for(p,1))}" width="1000" height="1500"{ld}>
      <img class="m2" src="{pimg(p,2)}" alt="" width="1000" height="1500" loading="lazy">
      <span class="idx">N°{n2(NUM[p['slug']])}</span>{badge}
    </a>
    <button class="fav" type="button" data-fav="{p['slug']}" aria-label="Ajouter {esc(p['name'])} aux favoris" aria-pressed="false">{ic('heart')}</button>
    <button class="quick" type="button" data-add="{p['slug']}">Ajout rapide <span>+</span></button>
  </div>
  <div class="card-info">
    <p class="card-meta">{esc(p['label'])}</p>
    <h3 class="card-name"><a href="produit-{p['slug']}.html">{esc(p['name'])}</a></h3>
    <p class="card-price">{price(p['price'])}</p>
  </div>
</article>'''


def cards(slugs):
    return "\n".join(card(BY_SLUG[s]) for s in slugs)


NAV = [("index", "index.html", "Accueil"), ("boutique", "boutique.html", "Boutique"),
       ("collections", "collections.html", "Collections"), ("histoire", "histoire.html", "Notre histoire"),
       ("aide", "aide.html", "Aide")]


def header(page):
    def cls(k):
        return ' class="active"' if k == page else ""
    sub_types = "".join(f'<a href="boutique.html?type={k}">{v}<span>{sum(1 for p in PRODUCTS if p["type"]==k)}</span></a>' for k, v in TYPES)
    sub_cols = "".join(f'<a href="collections.html#{k}">{v["name"]}<span>{sum(1 for p in PRODUCTS if p["collection"]==k)}</span></a>' for k, v in COLLECTIONS.items())
    return f'''<a class="skip" href="#contenu">Aller au contenu</a>
<div class="announce"><p><span class="dot"></span><span class="am">Livraison offerte dès {CURRENCY} {FREE_SHIPPING}</span><i>/</i><span class="am">Pochette cadeau &amp; carte-histoire offertes</span><i>/</i><span class="am">Retours sous 30 jours</span></p></div>
<header class="site-header">
  <div class="hdr-inner">
    <div class="hdr-left">
      <button class="icon-btn menu-btn" type="button" data-open="menu" aria-label="Ouvrir le menu">{ic('menu')}</button>
      <nav class="nav" aria-label="Navigation principale">
        <div class="has-mega">
          <a href="boutique.html"{cls('boutique')}>Boutique</a>
          <div class="mega" role="menu">
            <div class="mega-in">
              <div class="mega-col"><p class="mono">Par style</p>{sub_types}<a href="boutique.html" class="all">Tout voir {ic('arrow')}</a></div>
              <div class="mega-col"><p class="mono">Par collection</p>{sub_cols}<a href="boutique.html?filter=nouveau" class="all">Nouveautés {ic('arrow')}</a></div>
              <a class="mega-feature" href="collections.html#aura"><img src="{photo('tile-statement')}" alt="" width="900" height="1350" loading="lazy"><span class="mono">Collection Aura</span><strong>Sculpturales · Soirées</strong></a>
              <a class="mega-feature" href="histoire.html"><img src="{photo('story')}" alt="" width="1200" height="1500" loading="lazy"><span class="mono">La maison</span><strong>Chaque boucle, un prénom</strong></a>
            </div>
          </div>
        </div>
        <a href="boutique.html?filter=nouveau">Nouveautés</a>
        <a href="collections.html"{cls('collections')}>Collections</a>
        <a href="histoire.html"{cls('histoire')}>Notre histoire</a>
      </nav>
    </div>
    <a class="logo" href="index.html" aria-label="MAGALAÏ — accueil"><img src="assets/img/logo/magalai-bordeaux.png" alt="MAGALAÏ" width="1800" height="429"></a>
    <div class="hdr-right">
      <nav class="nav nav-r" aria-label="Aide"><a href="aide.html"{cls('aide')}>Aide</a></nav>
      <button class="icon-btn" type="button" data-open="search" aria-label="Rechercher">{ic('search')}</button>
      <a class="icon-btn fav-link" href="boutique.html?filter=favoris" aria-label="Mes favoris">{ic('heart')}<span class="count" data-fav-count data-n="0">0</span></a>
      <button class="icon-btn" type="button" data-open="cart" aria-label="Ouvrir le panier">{ic('bag')}<span class="count" data-cart-count data-n="0">0</span></button>
    </div>
  </div>
</header>'''


def drawers():
    mm = "".join(f'<a href="{h}">{t}</a>' for _, h, t in NAV)
    mm_types = "".join(f'<a href="boutique.html?type={k}">{v}</a>' for k, v in TYPES)
    return f'''<div class="overlay" data-close></div>
<aside class="drawer drawer-cart" id="cart" aria-label="Panier" aria-hidden="true">
  <div class="drawer-head"><h2>Panier</h2><button class="icon-btn" type="button" data-close aria-label="Fermer">{ic('close')}</button></div>
  <div class="ship-bar"><p data-ship-msg></p><div class="bar"><i data-ship-fill></i></div></div>
  <div class="drawer-body" data-cart-items></div>
  <div class="drawer-foot" data-cart-foot>
    <div class="row"><span>Sous-total</span><strong data-cart-subtotal>{CURRENCY} 0</strong></div>
    <p class="note">Livraison et taxes calculées à l'étape suivante. Chaque paire arrive avec la carte de son histoire.</p>
    <a class="btn btn-dark block" href="commande.html">Passer commande</a>
    <button class="btn-text" type="button" data-close>Continuer mes achats</button>
  </div>
</aside>
<aside class="drawer drawer-left" id="menu" aria-label="Menu" aria-hidden="true">
  <div class="drawer-head"><span class="mm-title">Menu</span><button class="icon-btn" type="button" data-close aria-label="Fermer">{ic('close')}</button></div>
  <div class="drawer-body mm"><div class="mm-main">{mm}</div><p class="mono mm-label">Par style</p><div class="mm-sub">{mm_types}<a href="boutique.html?filter=nouveau">Nouveautés</a></div></div>
</aside>
<div class="search" id="search" aria-hidden="true" role="dialog" aria-label="Recherche">
  <div class="search-box">
    <div class="search-top">{ic('search')}<input type="search" id="q" placeholder="Rechercher un prénom, un style…" autocomplete="off" aria-label="Rechercher"><button class="icon-btn" type="button" data-close aria-label="Fermer">{ic('close')}</button></div>
    <div class="search-results" id="results"></div>
  </div>
</div>
<div class="toast" role="status" aria-live="polite"></div>
<div class="cursor" aria-hidden="true"><i></i><span></span></div>'''


def footer():
    t = "".join(f'<li><a href="boutique.html?type={k}">{v}</a></li>' for k, v in TYPES)
    c = "".join(f'<li><a href="collections.html#{k}">{v["name"]}</a></li>' for k, v in COLLECTIONS.items())
    return f'''<footer class="site-footer">
  <div class="container foot-grid">
    <div class="foot-brand">
      <img src="assets/img/logo/magalai-or.png" alt="MAGALAÏ" width="1800" height="429">
      <p class="foot-tag">{TAGLINE}.</p>
      <form class="news-mini" data-newsletter><label class="sr" for="fn">E-mail</label><input id="fn" type="email" required placeholder="Votre e-mail"><button type="submit" aria-label="S'inscrire">{ic('arrow')}</button></form>
      <p class="fine">−10 % sur votre première commande en vous inscrivant.</p>
    </div>
    <div><h4>Boutique</h4><ul>{t}<li><a href="boutique.html?filter=nouveau">Nouveautés</a></li></ul></div>
    <div><h4>Collections</h4><ul>{c}</ul></div>
    <div><h4>La maison</h4><ul><li><a href="histoire.html">Notre histoire</a></li><li><a href="aide.html#livraison">Livraison</a></li><li><a href="aide.html#retours">Retours</a></li><li><a href="aide.html#faq">Questions fréquentes</a></li><li><a href="aide.html#contact">Contact</a></li></ul></div>
  </div>
  <div class="foot-giant" aria-hidden="true"><img src="assets/img/logo/magalai-or.png" alt="" width="1800" height="429" loading="lazy"></div>
  <div class="container foot-bottom">
    <p>© 2026 MAGALAÏ <i>/</i> <a href="legal.html">Mentions légales</a> <i>/</i> <a href="legal.html#cgv">CGV</a> <i>/</i> <a href="legal.html#confidentialite">Confidentialité</a></p>
    <ul class="pay" aria-label="Moyens de paiement"><li>Visa</li><li>Mastercard</li><li>TWINT</li><li>PayPal</li></ul>
  </div>
</footer>'''


def layout(page, title, desc, body, extra_head="", extra_js=""):
    full_title = title if "MAGALAÏ" in title else f"{title} — MAGALAÏ"
    site_ld = ""
    if page == "index":
        org = {"@context": "https://schema.org", "@graph": [
            {"@type": "Organization", "@id": SITE_URL + "/#org", "name": "MAGALAÏ", "url": SITE_URL + "/",
             "logo": SITE_URL + "/assets/img/logo/magalai-bordeaux.png", "slogan": TAGLINE,
             "description": "Boucles d'oreilles en acier inoxydable, finition dorée. Chaque paire porte le prénom d'une femme."},
            {"@type": "WebSite", "@id": SITE_URL + "/#site", "url": SITE_URL + "/", "name": "MAGALAÏ", "inLanguage": "fr-CH",
             "publisher": {"@id": SITE_URL + "/#org"}}]}
        site_ld = '<script type="application/ld+json">' + json.dumps(org, ensure_ascii=False) + '</script>'
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="theme-color" content="#5A0B16">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<link rel="canonical" href="{SITE_URL}/{CUR if CUR != 'index.html' else ''}">
<meta property="og:type" content="{'product' if page == 'produit' else 'website'}">
<meta property="og:site_name" content="MAGALAÏ">
<meta property="og:locale" content="fr_CH">
<meta property="og:url" content="{SITE_URL}/{CUR if CUR != 'index.html' else ''}">
<meta property="og:image" content="{SITE_URL}/assets/img/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="MAGALAÏ — boucles d'oreilles dorées, chaque paire porte un prénom">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(full_title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{SITE_URL}/assets/img/og-image.jpg">
{site_ld}
<link rel="icon" type="image/png" href="assets/img/logo/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
{extra_head}
</head>
<body data-page="{page}">
{header(page)}
<main id="contenu">
{body}
</main>
{footer()}
{drawers()}
<script src="assets/products.js"></script>
{extra_js}<script src="assets/main.js"></script>
</body>
</html>'''


def promises():
    items = [("truck", "Livraison offerte", f"Dès {CURRENCY} {FREE_SHIPPING} d'achat en Suisse"),
             ("shield", "Acier inoxydable", "Résiste à l'eau et à la transpiration"),
             ("return", "Retours 30 jours", "Simples et gratuits en Suisse"),
             ("lock", "Paiement sécurisé", "Carte, TWINT ou PayPal")]
    li = "".join(f'<li>{ic(i)}<div><strong>{t}</strong><span>{d}</span></div></li>' for i, t, d in items)
    return f'<section class="promises"><ul class="container">{li}</ul></section>'


def newsletter():
    return f'''<section class="newsletter">
  <div class="container nl-inner">
    <div><p class="mono">La lettre de Magalaï</p><h2>Les nouvelles histoires, <em>avant tout le monde.</em></h2></div>
    <form class="nl-form" data-newsletter><label class="sr" for="nl">Votre e-mail</label><input id="nl" type="email" required placeholder="Votre adresse e-mail"><button class="btn btn-dark" type="submit">S'inscrire</button><p class="fine">−10 % sur votre première commande. Désinscription à tout moment.</p></form>
  </div>
</section>'''


def ticker(extra=""):
    names = "".join(f'<span class="{"o" if i % 2 else ""}">{p["name"]}</span><i>✦</i>' for i, p in enumerate(PRODUCTS))
    return f'<div class="ticker{extra}" aria-hidden="true"><div class="ticker-track">{names}{names}</div></div>'


def section_head(kicker, title, link=None, href=None):
    lk = f'<a class="link-arrow" href="{href}">{link} {ic("arrow")}</a>' if link else ""
    return f'<div class="section-head"><div><p class="mono">{kicker}</p><h2>{title}</h2></div>{lk}</div>'


# ───────────────────────── pages ─────────────────────────
def nk_block(slug, model, stone, macro, style_label, band_text, rev=False):
    p = BY_SLUG[slug]
    r = " rev" if rev else ""
    feats = [("gem", "Design", "unique"), ("leaf", "Style", style_label), ("spark", "Finition", "dorée brillante"), ("heart", "Fait pour vous accompagner", "au quotidien")]
    fl = "".join(f'<li>{ic(i)}<span>{a}<br>{b}</span></li>' for i, a, b in feats)
    return f'''<div class="nk-block">
  <div class="nk-row{r}">
    <div class="nk-img img-reveal"><img src="{photo(model)}" alt="Boucles d'oreilles {p['name']} portées, collection Magalaï" loading="lazy" width="1000" height="866"></div>
    <div class="nk-text reveal">
      <p class="mono">Collection Magalaï <i>/</i> Bijoux qui vous ressemblent</p>
      <h2 class="nk-title">{p['name'].upper()}</h2>
      <p class="nk-tag">{esc(p['tagline'])}</p>
      <p class="nk-body">{esc(p['story'][0])}</p>
      <div class="cta-row"><button class="btn btn-dark" type="button" data-add="{slug}">Ajouter au panier {ic('arrow')}</button><a class="btn btn-outline" href="produit-{slug}.html">Voir la fiche</a></div>
    </div>
  </div>
  <ul class="nk-feats">{fl}</ul>
  <div class="nk-band{r}">
    <div class="nk-b-img img-reveal"><img src="{photo(stone)}" alt="Les boucles {p['name']} posées sur de la pierre" loading="lazy" width="800" height="780"></div>
    <div class="nk-b-text"><span class="nk-rule"></span><h3>Des détails qui font la différence</h3><span class="nk-rule"></span><p>{band_text}</p></div>
    <div class="nk-b-img img-reveal late"><img src="{photo(macro)}" alt="Détail de la finition des boucles {p['name']}" loading="lazy" width="800" height="760"></div>
  </div>
</div>'''


def nk_section():
    return f'''<section class="nk">
  <div class="container">
    {nk_block("nala", "nk-nala-model", "nk-nala-stone", "nk-nala-macro", "contemporain", "Des lignes graphiques et une finition dorée éclatante pour un bijou qui attire la lumière et sublime chaque instant.")}
    {nk_block("amara", "nk-amara-model", "nk-amara-stone", "nk-amara-macro", "bohème chic", "Un motif floral ajouré, une sphère lumineuse et une touche de couleur pour un bijou plein de caractère.", True)}
  </div>
</section>'''


def page_index():
    slides = []
    for i, (slug, fx, fy) in enumerate(HERO):
        p = BY_SLUG[slug]
        slides.append({"n": n2(NUM[slug]), "slug": slug, "name": p["name"], "desc": p["label"], "tag": p["tagline"],
                       "price": price(p["price"]), "href": f"produit-{slug}.html",
                       "coll": COLLECTIONS[p["collection"]]["name"], "fx": fx, "fy": fy, "img": photo(f"hero-{i+1}")})
    fb = "".join(f'<figure class="hero-fb{" on" if i == 0 else ""}"><img src="{s["img"]}" alt="Boucles {s["name"]}, portrait" width="1000" height="1500"{"" if i == 0 else " loading=lazy"}></figure>' for i, s in enumerate(slides))
    ticks = "".join(f'<button type="button" class="tick{" on" if i == 0 else ""}" data-go="{i}" aria-label="Diapositive {i+1}"><i></i></button>' for i in range(len(slides)))
    s0 = slides[0]
    new = [p["slug"] for p in PRODUCTS if p["badge"] == "Nouveau"]
    pref = ["lina", "clara", "ines", "zuri", "elena", "ava", "sofia"]

    quiz_btn = "".join(
        f'<button class="chip{" on" if i == 0 else ""}" type="button" data-mood="{k}" aria-pressed="{"true" if i == 0 else "false"}">{lbl}</button>'
        for i, (k, lbl, _, _) in enumerate(MOODS))
    quiz_res = ""
    for i, (k, lbl, slug, txt) in enumerate(MOODS):
        p = BY_SLUG[slug]
        quiz_res += f'''<div class="quiz-res{" on" if i == 0 else ""}" data-res="{k}">
  <a class="quiz-img" href="produit-{slug}.html"><img src="{pimg(p,2)}" alt="{esc(alt_for(p,2))}" loading="lazy" width="1000" height="1500"></a>
  <div><p class="mono">Vous êtes {esc(p['name'])}</p><h3>{esc(p['name'])}, <em>{esc(p['tagline'].rstrip('.').lower())}.</em></h3><p class="q-txt">{esc(txt)}</p>
  <p class="q-meta">{esc(p['label'])} <i>/</i> {price(p['price'])}</p>
  <a class="btn btn-white" href="produit-{slug}.html">Découvrir {esc(p['name'])}</a></div></div>'''

    tiles = ""
    for i, (k, lbl) in enumerate(TYPES, 1):
        cnt = sum(1 for p in PRODUCTS if p["type"] == k)
        tiles += f'''<a class="tile" href="boutique.html?type={k}"><img src="{photo('tile-'+k)}" alt="{lbl}" loading="lazy" width="900" height="1350">
  <div class="tile-label"><span class="mono">{n2(i)}</span><h3>{lbl}</h3><span class="tile-count">{cnt} modèles {ic('arrow')}</span></div></a>'''

    panels = ""
    for i, (k, c) in enumerate(COLLECTIONS.items(), 1):
        panels += f'''<a class="panel" href="collections.html#{k}"><img src="{photo('coll-'+k)}" alt="Collection {c['name']}" loading="lazy" width="1000" height="1500">
  <div class="panel-in"><span class="mono">Collection {n2(i)}</span><h3>{c['name']}</h3><p>{esc(c['short'])}</p><span class="link-arrow light">Découvrir {ic('arrow')}</span></div></a>'''

    comm = "".join(f'<a href="#" aria-label="Photo communauté {i}"><img src="{photo("comm-"+str(i))}" alt="" loading="lazy" width="700" height="1050"></a>' for i in range(1, 7))
    naima = BY_SLUG["aaliyah"]

    body = f'''
<section class="hero" data-hero data-slides='{esc(json.dumps(slides, ensure_ascii=False))}' aria-roledescription="carrousel" aria-label="Sélection du moment">
  <h1 class="sr">MAGALAÏ — boucles d'oreilles dorées. {TAGLINE}.</h1>
  <div class="hero-grid">
    <div class="hero-copy">
      <p class="mono hero-eyebrow"><span data-hero-n>N°{s0['n']}</span><i>/</i><span data-hero-coll>Collection {s0['coll']}</span></p>
      <p class="hero-name" data-hero-name aria-live="polite">{s0['name']}</p>
      <p class="hero-tag" data-hero-tag>{esc(s0['tag'])}</p>
      <p class="hero-meta"><span data-hero-desc>{esc(s0['desc'])}</span><i>/</i><span data-hero-price>{s0['price']}</span></p>
      <div class="cta-row"><a class="btn btn-dark" data-hero-link href="{s0['href']}">Découvrir {ic('arrow')}</a><a class="btn btn-outline" href="boutique.html">Toute la boutique</a></div>
      <div class="hero-controls">
        <button class="ctrl" type="button" data-prev aria-label="Précédent">{ic('arrow-l')}</button>
        <div class="ticks">{ticks}</div>
        <button class="ctrl" type="button" data-next aria-label="Suivant">{ic('arrow')}</button>
        <span class="count-big mono"><b data-hero-idx>01</b>/{n2(len(slides))}</span>
      </div>
    </div>
    <div class="hero-stage" data-stage>
      <canvas id="gl" aria-hidden="true"></canvas>
      <div class="hero-fallback">{fb}</div>
      <div class="hud" aria-hidden="true">
        <span class="c tl"></span><span class="c tr"></span><span class="c bl"></span><span class="c br"></span>
        <span class="hud-top mono">FIG.<b data-hero-fig>01</b> — {BRAND}</span>
        <span class="hud-xy mono">X <b data-x>0.50</b> · Y <b data-y>0.50</b></span>
        <span class="hud-side mono">{TAGLINE.upper()} — GENÈVE</span>
        <svg class="ring" viewBox="0 0 200 200"><defs><path id="rc" d="M100,100 m-80,0 a80,80 0 1,1 160,0 a80,80 0 1,1 -160,0"/></defs><text><textPath href="#rc" textLength="500" lengthAdjust="spacing">MAGALAÏ ✦ EVERY EARRING TELLS HER STORY ✦ MAGALAÏ ✦ </textPath></text></svg>
      </div>
    </div>
  </div>
  <span class="scroll-cue mono" aria-hidden="true">Scroll</span>
</section>
{ticker()}

<section class="section">
  <div class="container">
    {section_head("Nouveautés", "Les nouvelles <em>venues</em>", "Tout voir", "boutique.html?filter=nouveau")}
    <div class="grid-products g4">{cards(new)}</div>
  </div>
</section>

{nk_section()}

<section class="section tight">
  <div class="container">
    {section_head("Par style", "Choisissez votre <em>silhouette</em>", "Toute la boutique", "boutique.html")}
    <div class="tiles">{tiles}</div>
  </div>
</section>

<section class="principle">
  <div class="container principle-in">
    <article class="reveal"><span class="mono">01</span><h3>Une femme, un prénom</h3><p>Chaque boucle est imaginée comme le portrait de quelqu'un : sa manière d'entrer dans une pièce, de rire, de se tenir.</p></article>
    <article class="reveal"><span class="mono">02</span><h3>Une carte-histoire</h3><p>Dans l'écrin, une carte raconte celle dont la paire porte le nom. Un cadeau qui a déjà quelque chose à dire.</p></article>
    <article class="reveal"><span class="mono">03</span><h3>La vôtre à écrire</h3><p>Portez-la comme un prénom que l'on choisit. Le reste de l'histoire, c'est vous.</p></article>
  </div>
</section>

<section class="section matiere">
  <div class="container mat-grid">
    <div class="mat-intro reveal">
      <p class="mono">La matière</p>
      <h2>Acier inoxydable, <em>fait pour durer.</em></h2>
      <p class="lead">Chaque paire est en acier inoxydable : un métal choisi pour sa résistance, afin qu'elle vous suive partout, tous les jours.</p>
      <div class="mat-stat"><b>10,5<small>%</small></b><span>de chrome minimum : le seuil qui fait d'un acier un acier « inoxydable ».</span></div>
    </div>
    <div class="mat-cards">
      <article class="reveal"><span class="mono">01</span>{ic('layers')}<h3>Une barrière invisible</h3><p>Au contact de l'air, le chrome forme une fine couche d'oxyde, compacte et adhérente, qui protège l'acier de la corrosion.</p></article>
      <article class="reveal"><span class="mono">02</span>{ic('drop')}<h3>Eau &amp; transpiration</h3><p>Douche, pluie, sueur, cosmétiques : l'acier inoxydable y résiste. Seuls les bains prolongés en piscine ou en mer sont à éviter.</p></article>
      <article class="reveal"><span class="mono">03</span>{ic('shield')}<h3>Sans rouille au quotidien</h3><p>Dans un usage normal, il ne rouille pas : vos boucles se portent jour après jour, avec un simple chiffon doux pour tout entretien.</p></article>
      <article class="reveal"><span class="mono">04</span>{ic('ring')}<h3>Solide, pour longtemps</h3><p>Il ne se déforme pas et se recycle à l'infini : des boucles pensées pour durer, et à garder.</p></article>
    </div>
  </div>
  <p class="container mat-note fine">Bien toléré par la plupart des peaux ; en cas d'allergie au nickel avérée, demandez l'avis d'un dermatologue. Comme toute finition dorée, la couleur gagne à être ménagée : évitez les produits abrasifs et le chlore.</p>
</section>

<section class="section">
  <div class="container">
    {section_head("Trois univers", "Les <em>collections</em>", "Toutes les collections", "collections.html")}
    <div class="panels">{panels}</div>
  </div>
</section>

<section class="section story-sec">
  <div class="container sec-head-m">{section_head("Notre histoire", "Magalaï, un surnom <em>devenu maison.</em>", "Lire la suite", "histoire.html")}</div>
  <div class="container split">
    <div class="split-media img-reveal"><img src="{photo('story')}" alt="Portrait, boucles d'oreilles dorées" loading="lazy" width="1200" height="1500"></div>
    <div class="split-copy reveal">
      <div class="copy-head"><p class="mono">Notre histoire</p>
      <h2>Magalaï, un surnom <em>devenu maison.</em></h2></div>
      <p>À l'adolescence, on m'appelait Magalaï. Un surnom tendre, un peu mystérieux, que je n'ai jamais voulu laisser derrière moi.</p>
      <p>Aujourd'hui, c'est le nom d'une maison de boucles d'oreilles où chaque paire porte le prénom d'une femme, et arrive avec la carte de son histoire. Bohème, chic, dorée : à l'image de celles qui les portent.</p>
      <p class="sign">Magali</p>
      <a class="btn btn-dark hide-m" href="histoire.html">Lire la suite {ic('arrow')}</a>
    </div>
  </div>
</section>

<section class="quiz">
  <div class="container">
    <p class="mono">Trouvez la vôtre</p>
    <h2>Quelle femme êtes-vous <em>aujourd'hui ?</em></h2>
    <div class="chips" role="group" aria-label="Humeur">{quiz_btn}</div>
    <div class="quiz-stage">{quiz_res}</div>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("Les préférées", "Celles que l'on porte <em>tous les jours</em>", "Voir la boutique", "boutique.html")}
    <div class="rail" data-rail>{cards(pref)}</div>
  </div>
</section>

<section class="gift">
  <div class="container sec-head-m">{section_head("Offrir", "Un bijou, <em>une histoire</em> à offrir.", "Choisir un cadeau", "boutique.html")}</div>
  <div class="container gift-grid">
    <div class="gift-media img-reveal"><img src="{photo('pochette')}" alt="Pochette en velours bordeaux MAGALAÏ et boucles d'oreilles dorées" loading="lazy" width="900" height="854"></div>
    <div class="gift-copy reveal">
      <div class="copy-head"><p class="mono">Offrir</p>
      <h2>Un bijou, <em>une histoire</em> à offrir.</h2></div>
      <p>Chaque création MAGALAÏ porte le prénom d'une femme, symbole de force, de beauté et d'inspiration. Elle est glissée dans une pochette en velours bordeaux, accompagnée de la carte qui raconte la femme dont elle porte le prénom. Ajoutez un message manuscrit : nous l'écrivons pour vous.</p>
      <ul class="ticks-list"><li>{ic('check')} Écrin &amp; carte-histoire inclus</li><li>{ic('check')} Message manuscrit en option</li><li>{ic('check')} Livraison offerte dès {CURRENCY} {FREE_SHIPPING}</li></ul>
      <a class="btn btn-dark hide-m" href="boutique.html">Choisir un cadeau {ic('arrow')}</a>
    </div>
  </div>
</section>

<section class="section community">
  <div class="container">
    {section_head("@magalai", "Portées par <em>vous</em>", "Suivre sur Instagram", "#")}
    <div class="comm-grid">{comm}</div>
  </div>
</section>
{promises()}
{newsletter()}
'''
    return layout("index", "MAGALAÏ — Boucles d'oreilles dorées en acier inoxydable",
                  "Boucles d'oreilles dorées en acier inoxydable, résistantes à l'eau et à la sueur. Chaque paire porte le prénom d'une femme. Livraison offerte dès CHF 120.",
                  body, extra_js='<script src="assets/hero-data.js"></script>\n')


def page_boutique():
    chips = '<button class="chip on" type="button" data-type="all">Tout</button>' + "".join(
        f'<button class="chip" type="button" data-type="{k}">{v}</button>' for k, v in TYPES)
    cols = '<option value="all">Toutes les collections</option>' + "".join(
        f'<option value="{k}">{c["name"]}</option>' for k, c in COLLECTIONS.items())
    grid = []
    for i, p in enumerate(PRODUCTS):
        grid.append(card(p))
    edito = f'''<aside class="card-edito" data-edito>
  <a href="collections.html#aura"><img src="{photo('edito')}" alt="" loading="lazy" width="1000" height="1500">
  <div><span class="mono">Collection Aura</span><h3>Sculpturales, <em>pour les soirées.</em></h3><span class="link-arrow light">Découvrir {ic('arrow')}</span></div></a>
</aside>'''
    grid.insert(6, edito)
    body = f'''
<section class="page-head">
  <div class="container">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a> <i>/</i> Boutique</nav>
    <h1 data-shop-title>Toutes les <em>boucles d'oreilles</em></h1>
    <p class="lead">{len(PRODUCTS)} modèles, {len(PRODUCTS)} prénoms. Choisissez celle qui vous ressemble.</p>
  </div>
</section>
<section class="shop">
  <div class="container">
    <div class="filters">
      <div class="chips" role="group" aria-label="Style">{chips}</div>
      <div class="selects">
        <label class="sel"><span class="sr">Collection</span><select id="f-col">{cols}</select></label>
        <label class="sel"><span class="sr">Prix</span><select id="f-price"><option value="all">Tous les prix</option><option value="0-70">Moins de CHF 70</option><option value="70-100">CHF 70 à 100</option><option value="100-999">Plus de CHF 100</option></select></label>
        <label class="sel"><span class="sr">Trier</span><select id="f-sort"><option value="featured">Sélection Magalaï</option><option value="new">Nouveautés</option><option value="asc">Prix croissant</option><option value="desc">Prix décroissant</option><option value="az">Prénom A–Z</option></select></label>
        <div class="density" role="group" aria-label="Densité"><button type="button" data-cols="3" aria-label="3 colonnes" class="on">{ic('grid2')}</button><button type="button" data-cols="4" aria-label="4 colonnes">{ic('grid4')}</button></div>
      </div>
    </div>
    <p class="result-count mono" data-count aria-live="polite"></p>
    <div class="grid-products g3" id="shop-grid">{"".join(grid)}</div>
    <div class="empty" id="empty" hidden>
      <h2>Aucune <em>boucle</em> ici pour l'instant.</h2>
      <p data-empty-msg>Essayez d'autres filtres, ou découvrez l'ensemble de la boutique.</p>
      <a class="btn btn-dark" href="boutique.html">Voir toute la boutique</a>
    </div>
  </div>
</section>
{promises()}
'''
    return layout("boutique", "Boutique", "Toutes les boucles d'oreilles MAGALAÏ : créoles, puces, pendantes et statement. Chaque paire porte le prénom d'une femme.", body)


def page_produit(p):
    col = COLLECTIONS[p["collection"]]
    gal = "".join(
        f'<button type="button" class="g-item g{n}" data-zoom="{pimg(p,n)}" aria-label="Agrandir la vue {n}"><img src="{pimg(p,n)}" alt="{esc(alt_for(p,n))}" width="1000" height="1500"{"" if n == 1 else " loading=lazy"}></button>'
        for n in (1, 2, 3))
    badge = f'<span class="badge badge-static">{p["badge"]}</span>' if p["badge"] else ""
    story = "".join(f"<p>{esc(t)}</p>" for t in p["story"])
    related = [x["slug"] for x in PRODUCTS if x["slug"] != p["slug"] and (x["collection"] == p["collection"] or x["type"] == p["type"])][:4]
    for x in PRODUCTS:
        if len(related) >= 4:
            break
        if x["slug"] != p["slug"] and x["slug"] not in related:
            related.append(x["slug"])
    fr = FRAGILE.get(p["slug"])
    spec_txt = (" " + ", ".join(x for x in (p["dim"], (p["weight"] + " la paire") if p["weight"] else None, p["clasp"]) if x) + ".") if (p["dim"] or p["weight"] or p["clasp"]) else ""
    frag_detail = (f"<p>Les {fr} sont plus délicats que l'acier : évitez les chocs et retirez la paire avant de vous laver.</p>" if fr else "")
    frag_care = (f"<p>Pour les {fr} : pas d'eau prolongée, pas de produits (parfum, crème), et un simple chiffon sec.</p>" if fr else "")
    purl = f"{SITE_URL}/produit-{p['slug']}.html"
    ld = {"@context": "https://schema.org", "@type": "Product", "name": f"Boucles d'oreilles {p['name']} — {p['label']}",
          "description": f"{p['tagline']} {p['label']} en acier inoxydable, finition dorée, collection {col['name']}.",
          "sku": f"MAG-{n2(NUM[p['slug']])}", "material": "Acier inoxydable", "color": "Doré", "category": "Boucles d'oreilles",
          "brand": {"@type": "Brand", "name": "MAGALAÏ"}, "url": purl,
          "image": [f"{SITE_URL}/{pimg(p,n)}" for n in (1, 2, 3)],
          "offers": {"@type": "Offer", "url": purl, "priceCurrency": CURRENCY, "price": str(p["price"]),
                     "itemCondition": "https://schema.org/NewCondition", "availability": "https://schema.org/InStock"}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE_URL + "/"},
        {"@type": "ListItem", "position": 2, "name": "Boutique", "item": SITE_URL + "/boutique.html"},
        {"@type": "ListItem", "position": 3, "name": p["name"], "item": purl}]}
    head = ('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>\n'
            '<script type="application/ld+json">' + json.dumps(bc, ensure_ascii=False) + '</script>')
    body = f'''
<section class="pdp" data-pdp="{p['slug']}">
  <div class="container">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a> <i>/</i> <a href="boutique.html">Boutique</a> <i>/</i> <a href="boutique.html?type={p['type']}">{TYPE_LABEL[p['type']]}</a> <i>/</i> {esc(p['name'])}</nav>
    <div class="pdp-grid">
      <div class="gallery-wrap"><div class="gallery">{badge}{gal}</div><div class="g-dots" aria-hidden="true"><i class="on"></i><i></i><i></i></div></div>
      <div class="info">
        <p class="mono">N°{n2(NUM[p['slug']])} <i>/</i> Collection {col['name']}</p>
        <h1>{esc(p['name'])}</h1>
        <p class="sub">{esc(p['label'])}</p>
        <ul class="mat-chips"><li>Acier inoxydable</li><li>Résiste à l'eau &amp; à la sueur</li><li>Ne rouille pas</li></ul>
        <p class="pdp-price">{price(p['price'])}</p>
        <p class="pdp-tag">« {esc(p['tagline'])} »</p>
        <ul class="specs">{"".join(f"<li><span>{k}</span>{v}</li>" for k, v in (("Dimension", p["dim"]), ("Poids", p["weight"]), ("Fermeture", p["clasp"])) if v)}<li><span>Matière</span>Acier inoxydable</li><li><span>Finition</span>Dorée</li></ul>
        <label class="gift-opt"><input type="checkbox" id="gift-chk"><span class="box">{ic('check')}</span><span>Offrir avec <strong>écrin &amp; message manuscrit</strong> <em>(offert)</em></span></label>
        <div class="buy">
          <div class="qty" role="group" aria-label="Quantité"><button type="button" data-q="-1" aria-label="Moins">{ic('minus')}</button><output id="qty">1</output><button type="button" data-q="1" aria-label="Plus">{ic('plus')}</button></div>
          <button class="btn btn-dark add" type="button" data-add="{p['slug']}" data-qty-from="#qty">Ajouter au panier <i>/</i> {price(p['price'])}</button>
          <button class="fav fav-lg" type="button" data-fav="{p['slug']}" aria-label="Ajouter aux favoris" aria-pressed="false">{ic('heart')}</button>
        </div>
        <p class="delivery">{ic('truck')}<span data-delivery>Livraison estimée sous 2 à 4 jours ouvrés</span></p>
        <ul class="mini-promises"><li>{ic('truck')} Livraison offerte dès {CURRENCY} {FREE_SHIPPING}</li><li>{ic('return')} Retours sous 30 jours</li><li>{ic('shield')} Acier inoxydable : eau, sueur, rouille</li></ul>
        <div class="accordion">
          <details open><summary>Son histoire{ic('plus')}</summary><div class="acc-body">{story}</div></details>
          <details><summary>Détails &amp; matière{ic('plus')}</summary><div class="acc-body"><p><strong>Acier inoxydable, finition dorée.</strong>{spec_txt}</p><p>Au moins 10,5 % de chrome : au contact de l'air, il forme une fine couche d'oxyde qui protège l'acier de la corrosion. Il résiste à l'eau, à la transpiration et aux cosmétiques, et ne rouille pas dans un usage normal.</p><p>Matière bien tolérée par la plupart des peaux ; en cas d'allergie au nickel avérée, demandez l'avis d'un dermatologue.</p>{frag_detail}</div></details>
          <details><summary>Livraison &amp; retours{ic('plus')}</summary><div class="acc-body"><p>Expédition sous 48 h ouvrées. 2 à 3 jours en Suisse, 4 à 7 jours en Europe. Livraison offerte dès {CURRENCY} {FREE_SHIPPING}.</p><p>Retours acceptés sous 30 jours, boucles non portées et dans leur emballage d'origine.</p></div></details>
          <details><summary>Entretien{ic('plus')}</summary><div class="acc-body"><p>Douche, pluie et sport ne leur font pas peur. Évitez les bains prolongés en piscine ou en mer (chlore, sel).</p>{frag_care}<p>Pour préserver l'éclat de la finition dorée : évitez les produits abrasifs, essuyez-les avec un chiffon doux et rangez-les dans leur écrin.</p></div></details>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="story-band">
  <div class="container story-in">
    <p class="mono">Elle s'appelle</p>
    <p class="big-name">{esc(p['name'])}</p>
    <div class="story-text">{story}</div>
    <p class="mono sign-line">{BRAND} <i>/</i> {esc(TAGLINE)}</p>
  </div>
</section>

<section class="section">
  <div class="container">
    {section_head("À associer", "Complétez <em>le look</em>", "Toute la boutique", "boutique.html")}
    <div class="grid-products g4">{cards(related)}</div>
  </div>
</section>
{promises()}
<div class="sticky-atc" aria-hidden="true"><div><strong>{esc(p['name'])}</strong><span>{price(p['price'])}</span></div><button class="btn btn-dark" type="button" data-add="{p['slug']}">Ajouter au panier</button></div>
<div class="lightbox" id="lb" hidden><button class="icon-btn lb-close" type="button" aria-label="Fermer">{ic('close')}</button><button class="icon-btn lb-prev" type="button" aria-label="Précédent">{ic('arrow-l')}</button><img src="" alt=""><button class="icon-btn lb-next" type="button" aria-label="Suivant">{ic('arrow')}</button></div>
'''
    return layout("produit", f"{p['name']} — {p['label']}", f"Boucles d'oreilles {p['name']} : {p['label']}, collection {col['name']}. Acier inoxydable doré, résistant à l'eau. CHF {p['price']}. {p['tagline']}", body, head)


def page_collections():
    blocks = ""
    for i, (k, c) in enumerate(COLLECTIONS.items(), 1):
        items = [p["slug"] for p in PRODUCTS if p["collection"] == k]
        rev = " rev" if i % 2 == 0 else ""
        blocks += f'''<section class="coll-block{rev}" id="{k}">
  <div class="container sec-head-m">{section_head("Collection " + n2(i), c["name"], "Voir la collection", "boutique.html?collection=" + k)}</div>
  <div class="container coll-grid">
    <a class="coll-media img-reveal" href="boutique.html?collection={k}"><img src="{photo('coll-'+k)}" alt="Collection {c['name']}" loading="lazy" width="1000" height="1500"></a>
    <div class="coll-copy reveal">
      <div class="copy-head"><p class="mono">Collection {n2(i)} <i>/</i> {c['kicker']}</p>
      <h2>{c['name']}</h2></div>
      <p class="mono m-kicker">{c['kicker']}</p>
      <p class="lead">{esc(c['short'])}</p>
      <p>{esc(c['long'])}</p>
      <a class="btn btn-dark hide-m" href="boutique.html?collection={k}">Voir la collection {ic('arrow')}</a>
    </div>
  </div>
  <div class="container"><div class="grid-products g4 mini">{cards(items)}</div></div>
</section>'''
    az = "".join(f'<a class="chip" href="produit-{p["slug"]}.html">{p["name"]}</a>' for p in sorted(PRODUCTS, key=lambda x: x["name"]))
    body = f'''
<section class="page-head big">
  <div class="container">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a> <i>/</i> Collections</nav>
    <h1>Trois univers, <em>quatorze femmes.</em></h1>
    <p class="lead">Chaque collection a son atmosphère. Chaque boucle, son prénom.</p>
  </div>
</section>
{blocks}
<section class="section tint">
  <div class="container center">
    <p class="mono">Les prénoms</p>
    <h2>Elles s'appellent…</h2>
    <div class="chips names-all">{az}</div>
  </div>
</section>
{newsletter()}
'''
    return layout("collections", "Collections", "Aura, Soleil, Muse : les trois collections MAGALAÏ de boucles d'oreilles dorées, bohèmes et chics.", body)


def page_histoire():
    body = f'''
<section class="page-head big">
  <div class="container">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a> <i>/</i> Notre histoire</nav>
    <h1>Un surnom, <em>une promesse,</em> quatorze prénoms.</h1>
    <p class="lead">L'histoire de MAGALAÏ commence avec un mot que l'on m'a donné à l'adolescence.</p>
  </div>
</section>
<section class="section tight">
  <div class="container duo">
    <div class="img-reveal"><img src="{photo('histoire-1')}" alt="Portrait, boucles d'oreilles dorées" loading="lazy" width="1200" height="1500"></div>
    <div class="img-reveal late"><img src="{photo('histoire-2')}" alt="Portrait en blanc" loading="lazy" width="1400" height="1400"></div>
  </div>
</section>
<section class="section">
  <div class="container prose-grid">
    <div class="reveal">
      <p class="mono">Le nom</p>
      <h2>Magalaï, <em>le nom qu'on me donnait.</em></h2>
    </div>
    <div class="prose reveal">
      <p>À l'adolescence, on m'appelait Magalaï. Un surnom qui glissait de Magali vers quelque chose de plus doux, de plus mystérieux, de plus à moi. Je l'ai gardé.</p>
      <p>Quand j'ai voulu créer ma propre ligne de boucles d'oreilles, je cherchais un nom qui ait une âme. Je n'ai pas eu à chercher longtemps : il était là depuis toujours.</p>
      <p>On y entend Magali. On y voit un tréma, comme un petit clin d'œil au milieu d'un mot. Et on y devine une histoire, parce que les plus beaux bijoux ne sont jamais muets.</p>
    </div>
  </div>
</section>
{ticker(" dark")}
<section class="section">
  <div class="container prose-grid">
    <div class="reveal">
      <p class="mono">Le concept</p>
      <h2>Chaque boucle porte le prénom <em>d'une femme.</em></h2>
    </div>
    <div class="prose reveal">
      <p>Chaque création MAGALAÏ porte le prénom d'une femme, symbole de force, de beauté et d'inspiration.</p>
      <p>Nala, Amara, Lina, Naïma… Chaque modèle est imaginé comme le portrait d'une femme : sa manière d'entrer dans une pièce, de rire, de se tenir.</p>
      <p>Vous ne choisissez plus « des créoles » ou « des pendantes » : vous choisissez celle qui vous ressemble aujourd'hui. Et dans l'écrin, une carte vous raconte son histoire — il ne reste qu'à écrire la vôtre.</p>
      <a class="btn btn-dark" href="collections.html">Découvrir les femmes Magalaï {ic('arrow')}</a>
    </div>
  </div>
</section>
<section class="section tint">
  <div class="container">
    {section_head("Notre signature", "Bohème, chic, <em>dorée.</em>")}
    <div class="values">
      <article><span class="mono">01</span><h3>Bohème</h3><p>Des volumes libres, des formes inspirées par la nature et le mouvement : des bijoux qui bougent avec vous, du marché du matin au dîner qui s'éternise.</p></article>
      <article><span class="mono">02</span><h3>Chic</h3><p>Des lignes pures, des détails soignés, une finition irréprochable. Une élégance qui n'a rien à prouver, pensée pour les femmes actives de 23 à 55 ans.</p></article>
      <article><span class="mono">03</span><h3>Dorée &amp; durable</h3><p>Une finition dorée sur acier inoxydable, un métal résistant à l'eau et à la transpiration : de la lumière aux oreilles, au quotidien.</p></article>
    </div>
  </div>
</section>
<section class="founder">
  <div class="container founder-in reveal">
    <p class="mono">Un mot de la fondatrice</p>
    <blockquote>« J'ai voulu des bijoux qui ressemblent aux femmes qui les portent : multiples, lumineuses, jamais tout à fait les mêmes d'un jour à l'autre. »</blockquote>
    <p class="sign">Magali</p>
    <a class="btn btn-dark" href="boutique.html">Découvrir la boutique {ic('arrow')}</a>
  </div>
</section>
{newsletter()}
'''
    return layout("histoire", "Notre histoire", "Magalaï est un surnom d'adolescence devenu une maison de boucles d'oreilles : chaque paire porte le prénom d'une femme.", body)


def page_aide():
    faq = "".join(f'<details><summary>{esc(q)}{ic("plus")}</summary><div class="acc-body"><p>{esc(a)}</p></div></details>' for q, a in FAQ)
    body = f'''
<section class="page-head">
  <div class="container">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a> <i>/</i> Aide</nav>
    <h1>Besoin d'<em>aide ?</em></h1>
    <p class="lead">Livraison, retours, entretien : tout ce qu'il faut savoir, et une vraie personne si vous préférez nous écrire.</p>
  </div>
</section>
<section class="section help">
  <div class="container help-grid">
    <aside class="help-nav" aria-label="Rubriques"><a href="#livraison">Livraison</a><a href="#retours">Retours &amp; échanges</a><a href="#matiere">Notre matière</a><a href="#entretien">Entretien</a><a href="#faq">Questions fréquentes</a><a href="#contact">Nous écrire</a></aside>
    <div class="help-content">
      <article id="livraison"><h2>Livraison</h2>
        <table class="tbl"><thead><tr><th>Destination</th><th>Délai</th><th>Tarif</th></tr></thead><tbody>
          <tr><td>Suisse</td><td>2 à 3 jours ouvrés</td><td>CHF 6.90 · offerte dès CHF {FREE_SHIPPING}</td></tr>
          <tr><td>Europe</td><td>4 à 7 jours ouvrés</td><td>CHF 12 · offerte dès CHF 180</td></tr>
          <tr><td>Express Suisse</td><td>Lendemain avant 12 h</td><td>CHF 15</td></tr></tbody></table>
        <p>Les commandes passées avant 14 h partent le jour même (jours ouvrés). Chaque colis est emballé avec soin : écrin, carte-histoire et papier de soie.</p></article>
      <article id="retours"><h2>Retours &amp; échanges</h2>
        <p>Vous avez 30 jours après réception pour nous retourner vos boucles, non portées et dans leur emballage d'origine. Écrivez-nous, nous vous envoyons l'étiquette de retour. Remboursement sous 5 jours ouvrés.</p>
        <p>Pour des raisons d'hygiène, les boucles d'oreilles portées ne sont ni reprises ni échangées.</p></article>
      <article id="matiere"><h2>Notre matière : l'acier inoxydable</h2>
        <p>Nos boucles sont en acier inoxydable. Par définition, cet acier contient au moins 10,5 % de chrome : au contact de l'air, le chrome forme une fine couche d'oxyde, invisible, compacte et adhérente, qui protège le métal de la corrosion.</p>
        <ul class="ticks-list"><li>{ic('check')} Résiste à l'eau, à la transpiration et aux cosmétiques.</li><li>{ic('check')} Ne rouille pas dans un usage normal et se porte tous les jours.</li><li>{ic('check')} Ne se déforme pas, et se recycle à l'infini.</li><li>{ic('check')} Bien toléré par la plupart des peaux (le nickel y est chimiquement lié et très peu libéré) ; en cas d'allergie avérée, demandez l'avis d'un dermatologue.</li></ul></article>
      <article id="entretien"><h2>Entretien</h2>
        <ul class="ticks-list"><li>{ic('check')} Douche, pluie et sport : pas de souci, l'acier inoxydable résiste à l'eau et à la sueur.</li><li>{ic('check')} Évitez les bains prolongés en piscine ou en mer : le chlore et le sel peuvent fragiliser la couche protectrice.</li><li>{ic('check')} Pour préserver l'éclat de la finition dorée : pas de produits abrasifs, un chiffon doux suffit.</li><li>{ic('check')} Rangez-les dans leur écrin après le port.</li></ul></article>
      <article id="faq"><h2>Questions fréquentes</h2><div class="accordion">{faq}</div></article>
      <article id="contact"><h2>Nous écrire</h2>
        <form class="form" data-contact>
          <div class="f2"><label>Prénom<input required name="prenom" autocomplete="given-name"></label><label>E-mail<input type="email" required name="email" autocomplete="email"></label></div>
          <label>Sujet<select name="sujet"><option>Une commande</option><option>Un conseil pour choisir</option><option>Un cadeau</option><option>Autre</option></select></label>
          <label>Votre message<textarea required name="msg" rows="5"></textarea></label>
          <button class="btn btn-dark" type="submit">Envoyer</button>
          <p class="form-ok" hidden>Merci ! Votre message est bien parti. Nous vous répondons sous 48 h ouvrées.</p>
        </form></article>
    </div>
  </div>
</section>
'''
    return layout("aide", "Aide", "Livraison, retours, entretien et questions fréquentes : toute l'aide MAGALAÏ.", body)


def page_commande():
    body = f'''
<section class="page-head slim">
  <div class="container">
    <h1>Votre <em>commande</em></h1>
    <ol class="steps" aria-label="Étapes"><li class="on">01 Informations</li><li>02 Livraison</li><li>03 Paiement</li></ol>
  </div>
</section>
<section class="section checkout">
  <div class="container co-grid">
    <form class="co-form" id="checkout" novalidate>
      <p class="demo-note mono">Maquette de démonstration — aucun paiement n'est réellement effectué.</p>
      <fieldset><legend>Contact</legend>
        <label>E-mail<input type="email" name="email" required autocomplete="email" placeholder="prenom@exemple.ch"></label>
        <label class="inline"><input type="checkbox" checked> Recevoir les nouvelles histoires de Magalaï</label></fieldset>
      <fieldset><legend>Adresse de livraison</legend>
        <div class="f2"><label>Prénom<input name="prenom" required autocomplete="given-name"></label><label>Nom<input name="nom" required autocomplete="family-name"></label></div>
        <label>Adresse<input name="adresse" required autocomplete="street-address"></label>
        <div class="f3"><label>Code postal<input name="cp" required autocomplete="postal-code"></label><label>Ville<input name="ville" required autocomplete="address-level2"></label><label>Pays<select name="pays"><option>Suisse</option><option>France</option><option>Belgique</option><option>Allemagne</option><option>Italie</option></select></label></div></fieldset>
      <fieldset><legend>Mode de livraison</legend>
        <label class="radio"><input type="radio" name="ship" value="std" checked><span><strong>Standard</strong> · 2 à 3 jours</span><em data-ship-std>CHF 6.90</em></label>
        <label class="radio"><input type="radio" name="ship" value="exp"><span><strong>Express</strong> · lendemain avant 12 h</span><em>CHF 15</em></label></fieldset>
      <fieldset><legend>Paiement</legend>
        <label class="radio"><input type="radio" name="pay" value="card" checked><span><strong>Carte bancaire</strong> · Visa, Mastercard</span></label>
        <label class="radio"><input type="radio" name="pay" value="twint"><span><strong>TWINT</strong></span></label>
        <label class="radio"><input type="radio" name="pay" value="paypal"><span><strong>PayPal</strong></span></label>
        <div class="card-fields"><label>Numéro de carte<input inputmode="numeric" placeholder="1234 5678 9012 3456"></label><div class="f2"><label>Expiration<input placeholder="MM / AA"></label><label>Code<input placeholder="CVC"></label></div></div></fieldset>
      <button class="btn btn-dark block" type="submit">Payer maintenant</button>
    </form>
    <aside class="co-sum" aria-label="Récapitulatif">
      <h2>Récapitulatif</h2>
      <div data-co-items></div>
      <label class="promo"><span class="sr">Code promo</span><input id="promo" placeholder="Code promo" autocomplete="off"><button type="button" id="promo-btn" class="btn btn-outline-d">Appliquer</button></label>
      <dl class="totals"><div><dt>Sous-total</dt><dd data-co-sub>—</dd></div><div class="disc" hidden><dt>Réduction −10 %</dt><dd data-co-disc>—</dd></div><div><dt>Livraison</dt><dd data-co-ship>—</dd></div><div class="grand"><dt>Total</dt><dd data-co-total>—</dd></div></dl>
      <p class="fine">{ic('lock')} Paiement sécurisé · Carte-histoire incluse</p>
    </aside>
    <div class="co-empty" hidden><h2>Votre panier est <em>vide.</em></h2><p>Ajoutez une paire pour continuer.</p><a class="btn btn-dark" href="boutique.html">Voir la boutique</a></div>
    <div class="co-done" hidden>
      <span class="done-ic">{ic('check')}</span>
      <h2>Merci <em data-done-name></em> !</h2>
      <p>Votre commande <strong data-done-ref></strong> est confirmée. Un e-mail de confirmation vous attend, et votre colis part sous 48 h.</p>
      <p class="fine">(Maquette : aucune commande n'a été enregistrée.)</p>
      <a class="btn btn-dark" href="index.html">Retour à l'accueil</a>
    </div>
  </div>
</section>
'''
    return layout("commande", "Commande", "Finalisez votre commande MAGALAÏ.", body, '<meta name="robots" content="noindex">')


def page_legal():
    body = '''
<section class="page-head"><div class="container"><nav class="crumbs"><a href="index.html">Accueil</a> <i>/</i> Mentions légales</nav><h1>Mentions <em>légales</em></h1><p class="lead">Page à compléter avant la mise en ligne.</p></div></section>
<section class="section"><div class="container prose narrow">
<h2 id="mentions">Éditeur du site</h2><p>MAGALAÏ — [raison sociale, forme juridique, adresse, numéro IDE / RC, e-mail]. Directrice de la publication : Magali.</p>
<h2 id="cgv">Conditions générales de vente</h2><p>[À rédiger : prix, commande, paiement, livraison, droit de rétractation et retours, garanties, droit applicable.]</p>
<h2 id="confidentialite">Confidentialité</h2><p>[À rédiger : données collectées, finalités, durée de conservation, droits des personnes (LPD / RGPD), cookies.]</p>
</div></section>
'''
    return layout("legal", "Mentions légales", "Mentions légales, CGV et confidentialité de MAGALAÏ.", body, '<meta name="robots" content="noindex">')


def page_404():
    global CUR
    CUR = "404.html"
    body = f'''
<section class="page-head"><div class="container"><p class="mono">Erreur 404</p><h1>Cette page s'est <em>égarée.</em></h1><p class="lead">Le lien est peut-être ancien. Retrouvez nos boucles d'oreilles dans la boutique.</p><div class="cta-row" style="margin-top:32px"><a class="btn btn-dark" href="index.html">Accueil</a><a class="btn btn-outline" href="boutique.html">Voir la boutique</a></div></div></section>
'''
    return layout("legal", "Page introuvable", "Page introuvable.", body, '<meta name="robots" content="noindex">')


def products_js():
    data = [{"slug": p["slug"], "name": p["name"], "label": p["label"], "type": p["type"],
             "typeLabel": TYPE_LABEL[p["type"]], "collection": COLLECTIONS[p["collection"]]["name"],
             "price": p["price"], "img": pimg(p, 1), "tagline": p["tagline"]} for p in PRODUCTS]
    return ("window.MAGALAI = " + json.dumps({"currency": CURRENCY, "freeShipping": FREE_SHIPPING, "products": data},
                                           ensure_ascii=False, indent=1) + ";\n")


def build(path, html_text):
    global CUR
    w(path, html_text)


def main():
    global CUR
    w("assets/products.js", products_js())
    pages = [("index.html", page_index, 1.0), ("boutique.html", page_boutique, 0.9), ("collections.html", page_collections, 0.8),
             ("histoire.html", page_histoire, 0.7), ("aide.html", page_aide, 0.6)]
    urls = []
    for f, fn, pr in pages:
        CUR = f; w(f, fn()); urls.append((f, pr))
    for p in PRODUCTS:
        CUR = f"produit-{p['slug']}.html"; w(CUR, page_produit(p)); urls.append((CUR, 0.8))
    CUR = "commande.html"; w(CUR, page_commande())
    CUR = "legal.html"; w(CUR, page_legal())
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for f, pr in urls:
        loc = SITE_URL + "/" + ("" if f == "index.html" else f)
        sm.append(f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    w("sitemap.xml", "\n".join(sm) + "\n")
    w("robots.txt", f"User-agent: *\nAllow: /\nDisallow: /commande.html\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    w(".nojekyll", "")
    w("404.html", page_404())
    print(f"OK — {7 + len(PRODUCTS)} pages, {len(PRODUCTS)} produits")


if __name__ == "__main__":
    main()
