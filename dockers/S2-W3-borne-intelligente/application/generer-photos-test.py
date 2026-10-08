"""
Generation de 9 photos factices pour la borne intelligente vision.
Chaque image fait 224x224 (la taille d'entree native de MobileNetV2),
avec une couleur de fond differente et le nom de l'animal ecrit au centre.

But : permettre a la borne de fonctionner du premier coup (UI + inference)
meme sans vraies photos sous la main. Les predictions du modele sur ces
images synthetiques seront forcement aberrantes (probablement "envelope",
"carton box" ou "menu"). C'est attendu : c'est une demo de pipeline,
pas une demo de precision.

Pour avoir des resultats utiles, il suffit de remplacer le contenu de
application/photos/ par de vraies photos (n'importe quel jpg) avant
le build, puis de relancer construire.sh.
"""

import os

from PIL import Image, ImageDraw, ImageFont

REPERTOIRE_SORTIE = "/borne/photos"

# Liste des animaux : nom de fichier -> (libelle affiche, couleur de fond RGB).
# Couleurs choisies pour bien se distinguer entre elles a l'oeil.
ANIMAUX = [
    ("01-beluga.jpg",   "Beluga",   (210, 230, 240)),
    ("02-orignal.jpg",  "Orignal",  (130, 100,  70)),
    ("03-renard.jpg",   "Renard",   (220, 130,  60)),
    ("04-papillon.jpg", "Papillon", (240, 180, 100)),
    ("05-phoque.jpg",   "Phoque",   (160, 170, 180)),
    ("06-lievre.jpg",   "Lievre",   (200, 190, 170)),
    ("07-bourdon.jpg",  "Bourdon",  (240, 200,  60)),
    ("08-lynx.jpg",     "Lynx",     (170, 150, 110)),
    ("09-crabe.jpg",    "Crabe",    (200,  80,  70)),
]


def chargerPolice(taille):
    """Charge une fonte DejaVu installee dans l'image Docker, fallback sur la fonte par defaut."""
    cheminsCandidats = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for unChemin in cheminsCandidats:
        if os.path.exists(unChemin):
            return ImageFont.truetype(unChemin, taille)
    return ImageFont.load_default()


def couleurTexteSurFond(couleurFond):
    """Choisit du texte clair ou fonce selon la luminosite du fond."""
    luminosite = (couleurFond[0] * 299 + couleurFond[1] * 587 + couleurFond[2] * 114) / 1000
    if luminosite > 160:
        return (40, 40, 40)
    return (245, 245, 245)


def dessinerTexteCentre(dessin, texte, police, positionY, couleurTexte, largeurImage):
    """Centre un texte horizontalement a la position Y donnee."""
    boiteTexte = dessin.textbbox((0, 0), texte, font=police)
    largeurTexte = boiteTexte[2] - boiteTexte[0]
    positionX = (largeurImage - largeurTexte) // 2
    dessin.text((positionX, positionY), texte, font=police, fill=couleurTexte)


def genererUnePhoto(nomFichier, libelle, couleurFond):
    """Genere une image 224x224 avec le libelle au centre et un sous-titre."""
    largeurImage = 224
    hauteurImage = 224
    image = Image.new("RGB", (largeurImage, hauteurImage), couleurFond)
    dessin = ImageDraw.Draw(image)

    couleurTexte = couleurTexteSurFond(couleurFond)

    # Petite bordure interieure pour donner du caractere a la vignette.
    dessin.rectangle(
        [(6, 6), (largeurImage - 7, hauteurImage - 7)],
        outline=couleurTexte,
        width=2,
    )

    policeTitre = chargerPolice(36)
    policeSousTitre = chargerPolice(14)

    dessinerTexteCentre(dessin, libelle, policeTitre, 80, couleurTexte, largeurImage)
    dessinerTexteCentre(dessin, "photo factice", policeSousTitre, 140, couleurTexte, largeurImage)
    dessinerTexteCentre(dessin, "remplace-moi", policeSousTitre, 162, couleurTexte, largeurImage)

    cheminCible = os.path.join(REPERTOIRE_SORTIE, nomFichier)
    image.save(cheminCible, "JPEG", quality=88)


def genererToutesLesPhotos():
    """Cree le repertoire de sortie et y depose les 9 jpegs synthetiques."""
    os.makedirs(REPERTOIRE_SORTIE, exist_ok=True)
    for nomFichier, libelle, couleurFond in ANIMAUX:
        genererUnePhoto(nomFichier, libelle, couleurFond)
    print(f"{len(ANIMAUX)} photos factices generees dans {REPERTOIRE_SORTIE}")


if __name__ == "__main__":
    genererToutesLesPhotos()
