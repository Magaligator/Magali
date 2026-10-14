# -*- coding: utf-8 -*-
"""Optimise les photos de référence (dossier « publier 250108 ») pour le site.
À lancer UNE fois : python3 prepare_images.py "<dossier source>"
Sortie : assets/img/produits/<prenom>-1/2/3.webp, assets/img/photos/*.webp, assets/hero-data.js
Tes propres photos : dépose <prenom>-1.jpg (etc.) dans assets/img/produits/ puis relance build.py.
"""
import os, sys, io, base64, json
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else "/Users/magalitshikudi/Documents/Projet/Maïda/Boucles d'oreilles/publier 250108"
files = sorted(f for f in os.listdir(SRC) if f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png')))
F = lambda i: files[i]   # index dans la liste triée du dossier source

# slug : (packshot, portrait associé, ambiance)
PRODUCTS = {
    "lina":     (43, 79, 74),
    "clara":    (49, 75, 40),
    "elena":    (31, 51, 28),
    "victoria": (33, 42, 39),
    "aaliyah":  (41, 78, 34),
    "ines":     (36, 54, 37),
    "zuri":     (46, 2, 34),
    "ava":      (53, 52, 27),
    "naima":    (55, 45, 58),
    "nora":     (57, 32, 77),
    "juliette": (76, 62, 29),
    "sofia":    (80, 26, 16),
}
PHOTOS = {  # nom : (index, largeur max)
    "hero-1": (78, 1000), "hero-2": (2, 1000), "hero-3": (62, 1000), "hero-4": (42, 1000),
    "tile-creoles": (79, 900), "tile-puces": (52, 900), "tile-pendantes": (75, 900), "tile-statement": (34, 900),
    "coll-aura": (54, 1000), "coll-soleil": (74, 1000), "coll-muse": (26, 1000),
    "story": (40, 1200), "offer": (37, 1100), "histoire-1": (39, 1200), "histoire-2": (38, 1200),
    "edito": (32, 1000),
    "comm-1": (27, 700), "comm-2": (28, 700), "comm-3": (29, 700), "comm-4": (15, 700), "comm-5": (16, 700), "comm-6": (24, 700),
}
HERO_FOCUS = {}  # point focal éventuel (géré dans le JS)


def save(idx, out, width, q=80):
    im = Image.open(os.path.join(SRC, F(idx))).convert("RGB")
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, "WEBP", quality=q, method=6)
    return im.size


prov = []
for slug, idxs in PRODUCTS.items():
    for n, i in enumerate(idxs, 1):
        out = os.path.join(ROOT, "assets", "img", "produits", f"{slug}-{n}.webp")
        save(i, out, 1000)
        prov.append(f"produits/{slug}-{n}.webp  <-  {F(i)}")
for name, (i, w) in PHOTOS.items():
    out = os.path.join(ROOT, "assets", "img", "photos", f"{name}.webp")
    save(i, out, w)
    prov.append(f"photos/{name}.webp  <-  {F(i)}")

# images du slider en data-URI (WebGL ne peut pas lire les fichiers locaux file:// directement)
data = []
for k in range(1, 5):
    im = Image.open(os.path.join(SRC, F(PHOTOS[f"hero-{k}"][0]))).convert("RGB")
    im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "WEBP", quality=74, method=6)
    data.append("data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode())
with open(os.path.join(ROOT, "assets", "hero-data.js"), "w") as f:
    f.write("window.MAGALAI_HERO=" + json.dumps(data) + ";\n")

with open(os.path.join(ROOT, "assets", "img", "SOURCES.txt"), "w", encoding="utf-8") as f:
    f.write("Photos de référence issues du dossier « publier 250108 » (moodboard).\n"
            "ATTENTION : ces visuels semblent provenir de sites/campagnes tiers. Ils servent de maquette ;\n"
            "remplace-les par tes propres photos (ou des visuels libres de droits / licenciés) avant toute mise en ligne.\n\n")
    f.write("\n".join(prov) + "\n")
print("OK", len(prov), "images")
