# -*- coding: utf-8 -*-
"""Intègre les visuels des collections NALA et AMARA (affiches + photos réelles).
Usage : python3 add_content.py  (lit ~/Downloads ; adapte les noms de fichiers ci-dessous si besoin)
Sortie : assets/img/produits/{nala,amara}-1/2/3.webp, assets/img/photos/nk-*.webp, pochette, hero-1..4, assets/hero-data.js
"""
import os, io, json, base64
from PIL import Image, ImageOps, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
DL = os.path.expanduser("~/Downloads")
PROD = os.path.join(ROOT, "assets", "img", "produits")
PH = os.path.join(ROOT, "assets", "img", "photos")


def find(part):
    names = sorted(f for f in os.listdir(DL) if part in f and not f.startswith("~"))
    return os.path.join(DL, names[-1])


def load(path, exif=False):
    im = Image.open(path)
    if exif:
        im = ImageOps.exif_transpose(im)
    return im.convert("RGB")


AMARA = load(find("Amara (1).png"))
NALA = load(find("collection NALA.png"))
R = load(os.path.join(DL, "IMG_0606 (1).jpeg"), True)   # AMARA : photo réelle
S = load(os.path.join(DL, "IMG_0603.jpeg"), True)       # NALA : photo réelle


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


# zones des affiches (le portrait AMARA est recadré au-dessus du texte incrusté)
a_model = AMARA.crop((0, 0, 602, 520)); n_model = NALA.crop((0, 0, 598, 630))
a_stone = AMARA.crop((0, 770, 392, 1150)); a_macro = AMARA.crop((672, 770, 1024, 1150))
n_stone = NALA.crop((0, 770, 392, 1150)); n_macro = NALA.crop((674, 770, 1024, 1150))
a_pouch = AMARA.crop((330, 1152, 1024, 1536))

# NALA : photo réelle (4:5), portrait, pose sur pierre
p("nala", 1, S.crop((0, 140, 3024, 3920)))
p("nala", 2, n_model.crop((14, 0, 598, 630)), 1000)
p("nala", 3, n_stone, 900)
# AMARA : photo réelle (4:5), portrait, détail de la photo réelle
p("amara", 1, R.crop((0, 200, 3024, 3980)))
p("amara", 2, a_model.crop((20, 0, 602, 520)), 1000)
p("amara", 3, R.crop((1250, 640, 2550, 2265)))

# visuels éditoriaux de l'accueil
ph("nk-nala-model", n_model, 1000); ph("nk-amara-model", a_model, 1000)
ph("nk-nala-stone", n_stone, 800); ph("nk-nala-macro", n_macro, 800)
ph("nk-amara-stone", a_stone, 800); ph("nk-amara-macro", a_macro, 800)
ph("pochette", a_pouch.crop((110, 0, 494, 384)), 900)

# slider : NALA et AMARA en tête, puis les deux portraits précédents
if not os.path.exists(os.path.join(PH, "_hero-prev-1.webp")):
    for i in (1, 2):
        os.replace(os.path.join(PH, f"hero-{i}.webp"), os.path.join(PH, f"_hero-prev-{i}.webp"))
prev = [Image.open(os.path.join(PH, f"_hero-prev-{i}.webp")).convert("RGB") for i in (1, 2)]
for i, im in enumerate([n_model, a_model, prev[0], prev[1]], 1):
    out(im, os.path.join(PH, f"hero-{i}.webp"), 1000 if im.width < 1000 else im.width, 84)
uris = []
for i in range(1, 5):
    im = Image.open(os.path.join(PH, f"hero-{i}.webp")).convert("RGB")
    im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "WEBP", quality=76, method=6)
    uris.append("data:image/webp;base64," + base64.b64encode(b.getvalue()).decode())
open(os.path.join(ROOT, "assets", "hero-data.js"), "w").write("window.MAGALAI_HERO=" + json.dumps(uris) + ";\n")
print("OK")
