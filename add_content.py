# -*- coding: utf-8 -*-
"""Intègre les visuels fournis (affiches NALA / KATE + photos réelles) dans le site.
Usage : python3 add_content.py  (lit ~/Downloads ; adapte les noms de fichiers ci-dessous si besoin)
Sortie : assets/img/produits/{kate,nala,amara}-1/2/3.webp, assets/img/photos/nk-*.webp, hero-1..4, assets/hero-data.js
"""
import os, io, json, base64
from PIL import Image, ImageOps, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
DL = os.path.expanduser("~/Downloads")
PROD = os.path.join(ROOT, "assets", "img", "produits")
PH = os.path.join(ROOT, "assets", "img", "photos")


def load(name, exif=False):
    im = Image.open(os.path.join(DL, name))
    if exif:
        im = ImageOps.exif_transpose(im)
    return im.convert("RGB")


NALA = load("Affiche éditoriale des boucles NALA.png")
KATE = load("Élégance sculpturale des boucles KATE.png")
R = load("IMG_0606 (1).jpeg", True)   # disques filigranés + cristaux (photo réelle)
S = load("IMG_0603.jpeg", True)       # KATE, photo réelle


def out(im, path, width, q=86, sharpen=True):
    if im.width != width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    if sharpen and width > 800:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "WEBP", quality=q, method=6)


def p(slug, n, im, w=1100):
    out(im, os.path.join(PROD, f"{slug}-{n}.webp"), w)


def ph(name, im, w):
    out(im, os.path.join(PH, f"{name}.webp"), w)


# zones des affiches (sans le texte incrusté « MAGALAÏ / BIJOUX QUI VOUS RESSEMBLENT »)
n_model = NALA.crop((0, 0, 602, 520)); k_model = KATE.crop((0, 0, 606, 520))
n_stone = NALA.crop((0, 770, 391, 1150)); n_macro = NALA.crop((676, 770, 1024, 1150))
k_stone = KATE.crop((0, 762, 468, 1158)); k_macro = KATE.crop((720, 762, 1024, 1158))
n_pouch = NALA.crop((330, 1152, 1024, 1536))

# KATE : photo réelle (recadrage 4:5), portée, détail
p("kate", 1, S.crop((0, 140, 3024, 3920)))
p("kate", 2, k_model.crop((20, 0, 606, 520)), 1000)
p("kate", 3, k_stone.crop((20, 0, 468, 396)), 900)
# NALA : visuels de l'affiche
p("nala", 1, n_model.crop((20, 0, 602, 520)), 1000)
p("nala", 2, n_stone, 800)
p("nala", 3, n_macro, 800)
# AMARA : photo réelle (recadrage 4:5) + deux détails
p("amara", 1, R.crop((0, 200, 3024, 3980)))
p("amara", 2, R.crop((1250, 640, 2550, 2265)))
p("amara", 3, R.crop((540, 1950, 1840, 3575)))

# visuels éditoriaux de l'accueil
ph("nk-nala-model", n_model, 1000); ph("nk-kate-model", k_model, 1000)
ph("nk-nala-stone", n_stone, 800); ph("nk-nala-macro", n_macro, 800)
ph("nk-kate-stone", k_stone, 900); ph("nk-kate-macro", k_macro, 700)
ph("pochette", n_pouch.crop((60, 0, 460, 384)), 900)

# slider : NALA et KATE en tête, puis les deux portraits précédents
if not os.path.exists(os.path.join(PH, "_hero-prev-1.webp")):
    for i in (1, 2):
        os.replace(os.path.join(PH, f"hero-{i}.webp"), os.path.join(PH, f"_hero-prev-{i}.webp"))
prev = [Image.open(os.path.join(PH, f"_hero-prev-{i}.webp")).convert("RGB") for i in (1, 2)]
for i, im in enumerate([n_model, k_model, prev[0], prev[1]], 1):
    out(im, os.path.join(PH, f"hero-{i}.webp"), 1000 if im.width < 1000 else im.width, 84)
uris = []
for i in range(1, 5):
    im = Image.open(os.path.join(PH, f"hero-{i}.webp")).convert("RGB")
    im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "WEBP", quality=76, method=6)
    uris.append("data:image/webp;base64," + base64.b64encode(b.getvalue()).decode())
open(os.path.join(ROOT, "assets", "hero-data.js"), "w").write("window.MAGALAI_HERO=" + json.dumps(uris) + ";\n")
print("OK")
