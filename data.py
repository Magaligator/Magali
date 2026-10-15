# -*- coding: utf-8 -*-
"""Catalogue fictif MAGALAÏ — modifie noms, prix, histoires ici puis relance `python3 build.py`."""

BRAND = "MAGALAÏ"
TAGLINE = "Every earring tells her story"
CURRENCY = "CHF"
FREE_SHIPPING = 120

TYPES = [
    ("creoles", "Créoles"),
    ("puces", "Puces"),
    ("pendantes", "Pendantes"),
    ("statement", "Statement"),
]

COLLECTIONS = {
    "aura": {
        "name": "Aura",
        "kicker": "Sculpturales · Soirées",
        "short": "Des pièces qui prennent la lumière, pour les soirs où l'on veut être regardée.",
        "long": ("Aura est la collection des grandes entrées. Sphères filigranées, éventails d'éclats, rayons de perles : "
                 "chaque pièce dessine un halo autour du visage et laisse à celle qui la porte tout l'espace pour raconter sa soirée."),
    },
    "soleil": {
        "name": "Soleil",
        "kicker": "Bohèmes · Solaires",
        "short": "La lumière dorée des étés sans fin : volumes généreux, ciselures et ailes qui suivent vos journées.",
        "long": ("Soleil est née d'un souvenir de lumière rasante. Des volumes libres, une finition dorée mate ou texturée, une allure "
                 "qui bouge avec vous : de la terrasse du matin au dîner qui s'étire, elles ne se démodent pas."),
    },
    "muse": {
        "name": "Muse",
        "kicker": "Fines · Du quotidien",
        "short": "Les indispensables : perles, dômes et cercles ajourés à porter tous les jours.",
        "long": ("Muse rassemble les pièces que l'on ne quitte plus. Précises, légères, faciles à associer : elles "
                 "installent une élégance discrète, celle qui n'a rien à prouver."),
    },
}

PRODUCTS = [
    dict(slug="nala", name="Nala", type="statement", collection="aura", price=149,
         badge="Nouveau", label="Boucles éventails ondulés",
         dim=None, weight=None, clasp=None,
         tagline="Une silhouette audacieuse, tout en élégance.",
         story=["Les boucles d'oreilles NALA se distinguent par leur design sculptural et contemporain. Leur forme ondulante aux reflets dorés apporte une touche de caractère et de sophistication à chaque tenue. Un bijou lumineux, pensé pour les femmes qui assument leur style avec élégance.",
                "Des lignes graphiques et une finition dorée éclatante pour un bijou qui attire la lumière et sublime chaque instant."]),
    dict(slug="amara", name="Amara", type="statement", collection="soleil", price=129,
         badge="Nouveau", label="Disques floraux ajourés",
         dim=None, weight=None, clasp=None,
         tagline="L'élégance qui ne passe pas inaperçue.",
         story=["Audacieuses, lumineuses et délicatement travaillées, les boucles d'oreilles AMARA apportent une touche de caractère à chaque tenue. Leur silhouette florale ajourée et leur sphère centrale à l'effet miroir captent la lumière, sublimées par de délicats détails colorés.",
                "Un motif floral ajouré, une sphère lumineuse et une touche de couleur pour un bijou plein de caractère."]),
    dict(slug="lina", name="Lina", type="creoles", collection="soleil", price=89,
         badge="Best-seller", label="Créoles sculptées",
         dim="Ø 32 mm", weight="4,4 g", clasp="Fermoir clic",
         tagline="Elle arrive la première, repart la dernière.",
         story=["Lina ne demande jamais la permission d'entrer dans une pièce. Elle entre, et la conversation "
                "se met à tourner autour d'elle.",
                "Ses créoles sculptées, ajourées comme une dentelle dorée, disent ce qu'elle n'a pas besoin de dire : "
                "elle sait où elle va. Le genre de pièce que l'on garde dix ans et que l'on ne prête à personne."]),
    dict(slug="clara", name="Clara", type="creoles", collection="muse", price=69,
         badge="Best-seller", label="Créoles ajourées",
         dim="Ø 30 mm", weight="2,6 g", clasp="Tige & papillon",
         tagline="La douceur qui a du caractère.",
         story=["Clara aime les détails que l'on découvre de près : un cercle doré, une dentelle de métal, "
                "une lumière qui glisse à chaque mouvement de tête.",
                "Discrète au bureau, éclatante dès que le soir tombe, elle passe d'une vie à l'autre sans jamais "
                "changer de boucles."]),
    dict(slug="elena", name="Éléna", type="creoles", collection="soleil", price=79,
         badge=None, label="Créoles croissant mat",
         dim="H 38 mm", weight="3,2 g", clasp="Tige & papillon",
         tagline="Elle écrit à la lune.",
         story=["Éléna garde un carnet sous l'oreiller pour les idées qui arrivent à minuit.",
                "Ses croissants dorés et mats, légers comme un souffle, accompagnent les rêveuses qui ont les pieds sur "
                "terre : celles qui finissent toujours par réaliser ce qu'elles ont écrit."]),
    dict(slug="victoria", name="Victoria", type="pendantes", collection="aura", price=149,
         badge="Nouveau", label="Pendantes sphères filigranées",
         dim="H 55 mm", weight="5,2 g", clasp="Tige & papillon",
         tagline="Les grandes soirées lui appartiennent.",
         story=["Victoria ne choisit pas entre élégance et audace : elle porte les deux, avec le même sourire.",
                "Ses sphères dorées et filigranées se balancent à chaque pas et dessinent une silhouette sur chaque épaule. "
                "À porter les cheveux relevés, le regard droit."]),
    dict(slug="aaliyah", name="Aaliyah", type="statement", collection="aura", price=129,
         badge=None, label="Boucles soleil et perles",
         dim="Ø 42 mm", weight="4,9 g", clasp="Tige & papillon",
         tagline="Elle porte le soleil à l'oreille.",
         story=["Aaliyah rayonne sans effort. Les gens s'approchent d'elle comme d'une fenêtre ouverte "
                "un matin de printemps.",
                "Des rayons dorés, des perles en gouttes : une pièce graphique qui transforme un simple col "
                "blanc en tenue de fête."]),
    dict(slug="ines", name="Inès", type="puces", collection="muse", price=79,
         badge="Best-seller", label="Puces fleur perlée",
         dim="Ø 22 mm", weight="2,8 g", clasp="Tige & papillon",
         tagline="L'élégance qui ne fait pas de bruit.",
         story=["Inès parle peu et se fait toujours entendre. Elle a compris très tôt que le raffinement "
                "tient dans la retenue.",
                "Une fleur dorée ourlée de petites perles, rien de plus : la puce qu'on porte tous les jours, avec tout, "
                "et qui fait toujours le même effet."]),
    dict(slug="zuri", name="Zuri", type="pendantes", collection="soleil", price=99,
         badge=None, label="Pendantes feuille ciselée",
         dim="H 44 mm", weight="4,1 g", clasp="Tige & papillon",
         tagline="Le soleil dans les cheveux.",
         story=["Zuri signifie « belle » en swahili. Elle n'a jamais eu besoin qu'on le lui rappelle.",
                "Une feuille dorée ciselée qui s'ouvre comme une fleur : un bijou d'été qui garde la chaleur "
                "de la journée jusqu'au soir."]),
    dict(slug="ava", name="Ava", type="puces", collection="muse", price=65,
         badge=None, label="Puces dôme spirale",
         dim="Ø 20 mm", weight="3,0 g", clasp="Tige & papillon",
         tagline="Petite, mais on ne voit qu'elle.",
         story=["Ava tient dans la paume d'une main et dans la mémoire de tous ceux qui l'ont croisée.",
                "Son dôme doré aux lignes en spirale épouse le lobe comme une seconde peau. À porter seule ou "
                "en accumulation, sans jamais les retirer."]),
    dict(slug="naima", name="Naïma", type="statement", collection="aura", price=119,
         badge="Nouveau", label="Éventail d'éclats",
         dim="H 48 mm", weight="3,8 g", clasp="Tige & papillon",
         tagline="Un éclat, une promesse.",
         story=["Naïma a le goût des soirées qui commencent tard et du rire qui éclate au milieu d'une phrase.",
                "Son éventail doré tapissé d'éclats se porte comme un secret que l'on ne cache pas vraiment : "
                "il accompagne les retrouvailles, les robes qui bougent, les nuits trop courtes."]),
    dict(slug="nora", name="Nora", type="pendantes", collection="aura", price=95,
         badge=None, label="Pendantes carré filigrane",
         dim="H 50 mm", weight="3,5 g", clasp="Tige & papillon",
         tagline="La ligne claire.",
         story=["Nora a une règle : ne garder que l'essentiel. Une phrase, une couleur, un bijou.",
                "Son carré doré ajouré comme une carte de géographie dessine un trait de lumière près du visage. "
                "Pour celles qui préfèrent les graphismes aux fioritures."]),
    dict(slug="juliette", name="Juliette", type="pendantes", collection="soleil", price=109,
         badge=None, label="Pendantes ailes ajourées",
         dim="H 58 mm", weight="2,4 g", clasp="Tige & papillon",
         tagline="Elle a les ailes qu'elle s'est données.",
         story=["Juliette n'a jamais attendu qu'on lui ouvre une porte : elle a construit la sienne.",
                "Ses ailes dorées, fines comme une nervure de feuille, ne pèsent presque rien. "
                "Une légèreté qui donne envie de partir."]),
    dict(slug="sofia", name="Sofia", type="puces", collection="muse", price=85,
         badge=None, label="Puces cône texturé",
         dim="H 30 mm", weight="3,6 g", clasp="Tige & papillon",
         tagline="La sagesse qui sourit.",
         story=["Sofia veut dire « sagesse ». La sienne a toujours été joyeuse, un peu insolente, très généreuse.",
                "Ses cônes dorés et texturés accrochent la lumière comme un grain de sable doré. "
                "Elles vont avec le lin, la soie, les cheveux qui s'échappent."]),
]

# humeur → boucle proposée
MOODS = [
    ("solaire", "Solaire", "aaliyah", "Vous entrez dans la pièce avec le sourire. Aaliyah rayonne avec vous, du premier café au dernier verre."),
    ("discrete", "Discrète", "ines", "Vous préférez la retenue. Inès, une fleur dorée ourlée de perles, ne fait jamais de bruit mais se remarque toujours."),
    ("audacieuse", "Audacieuse", "victoria", "Vous aimez qu'on vous regarde. Victoria dessine des sphères dorées sur chaque épaule."),
    ("romantique", "Romantique", "naima", "Vous croyez aux promesses. Naïma, un éventail d'éclats, accompagne les plus belles."),
]

# diapositives du slider d'accueil : (slug du produit lié, fichier hero, point focal x, y)
HERO = [
    ("nala", 0.60, 0.50),
    ("amara", 0.55, 0.50),
    ("aaliyah", 0.50, 0.46),
    ("zuri", 0.50, 0.42),
]

FAQ = [
    ("Quelle est la matière de vos boucles d'oreilles ?",
     "Nos boucles sont en acier inoxydable, un métal choisi pour sa résistance. Il contient au moins 10,5 % de chrome, qui forme au contact de l'air une fine couche d'oxyde protectrice : l'acier résiste à l'eau, à la transpiration et aux cosmétiques, et ne rouille pas dans un usage normal. La finition est dorée."),
    ("Puis-je les garder sous la douche, au sport ou à la piscine ?",
     "Oui pour la douche, la pluie et le sport : l'acier inoxydable résiste à l'eau et à la transpiration. On évite en revanche les bains prolongés en piscine ou en mer, car le chlore et le sel peuvent fragiliser la couche protectrice et ternir la finition dorée."),
    ("Conviennent-elles aux peaux sensibles ?",
     "Dans l'acier inoxydable, le nickel est chimiquement lié à l'alliage et très peu libéré : la matière est bien tolérée par la plupart des peaux. Elle n'est toutefois pas garantie sans risque en cas d'allergie au nickel avérée : au moindre doute, demandez l'avis d'un dermatologue."),
    ("Comment entretenir mes boucles ?",
     "L'acier inoxydable demande peu d'entretien : essuyez vos boucles avec un chiffon doux après le port et rangez-les dans leur écrin. Pour préserver l'éclat de la finition dorée, évitez les produits abrasifs, le chlore et les frottements."),
    ("Puis-je échanger ou retourner ma commande ?",
     "Oui, vous avez 30 jours après réception pour nous retourner vos boucles, non portées, dans leur emballage d'origine. Pour des raisons d'hygiène, les boucles portées ne sont ni reprises ni échangées."),
    ("Quels sont les délais de livraison ?",
     "Les commandes partent sous 48 h ouvrées. Comptez 2 à 3 jours en Suisse, 4 à 7 jours en Europe. Livraison offerte dès CHF 120 d'achat."),
    ("Comment fonctionne la pochette cadeau ?",
     "Chaque paire est livrée dans une pochette à cordon, accompagnée de la carte racontant l'histoire de la femme dont elle porte le prénom. Vous pouvez y ajouter un message manuscrit."),
    ("Proposez-vous des cartes cadeaux ?",
     "Bientôt. Écrivez-nous et nous vous aiderons à choisir un cadeau qui ressemble à la personne que vous aimez."),
]
