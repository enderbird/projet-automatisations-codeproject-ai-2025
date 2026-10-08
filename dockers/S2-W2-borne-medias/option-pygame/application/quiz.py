"""
Borne medias - Quiz Pygame
Zoo maritime du Bas-Saint-Laurent

Application kiosque qui pose des questions sur les especes des quatre pavillons :
foret, marin, prairie, voyageurs. Decor par pavillon dessine en primitives,
fond a vagues animees, etincelles sur bonne reponse.
"""

import math
import os
import random
import sys

import pygame

LARGEUR_ECRAN = 1280
HAUTEUR_ECRAN = 720

COULEUR_FOND_HAUT = (250, 244, 226)
COULEUR_FOND_BAS = (236, 224, 196)
COULEUR_TEXTE_PRINCIPAL = (40, 40, 42)
COULEUR_TEXTE_DOUX = (98, 96, 88)
COULEUR_TEXTE_INVERSE = (255, 253, 246)
COULEUR_BANNIERE = (31, 77, 44)
COULEUR_CARTE = (255, 253, 246)
COULEUR_CARTE_CONTOUR = (28, 28, 32)
COULEUR_CARTE_OMBRE = (30, 30, 30, 70)
COULEUR_REPONSE_FOND = (255, 253, 246)
COULEUR_REPONSE_BORDURE = (40, 40, 42)
COULEUR_REPONSE_SURVOL = (250, 240, 210)
COULEUR_REPONSE_BONNE = (39, 174, 96)
COULEUR_REPONSE_MAUVAISE = (210, 48, 48)
COULEUR_ACCENT = (210, 48, 48)
COULEUR_SURLIGNEMENT = (251, 207, 61)
COULEUR_BULLE_FOND = (255, 253, 246)
COULEUR_BULLE_CONTOUR = (28, 28, 32)
COULEUR_MASCOTTE_CORPS = (250, 250, 246)
COULEUR_MASCOTTE_OMBRE = (220, 222, 218)
COULEUR_MASCOTTE_TRAIT = (32, 32, 36)

COULEURS_PAVILLON = {
    "foret": (130, 160, 76),
    "marin": (61, 150, 189),
    "prairie": (189, 149, 58),
    "voyageurs": (151, 99, 58),
}

COULEURS_PAVILLON_DOUX = {
    "foret": (210, 224, 184),
    "marin": (188, 220, 234),
    "prairie": (234, 218, 174),
    "voyageurs": (220, 196, 168),
}

NOMS_PAVILLON = {
    "foret": "Pavillon foret",
    "marin": "Pavillon marin",
    "prairie": "Pavillon prairie",
    "voyageurs": "Pavillon voyageurs",
}

QUESTIONS = [
    {
        "pavillon": "marin",
        "enonce": "Quel mammifere blanc emblematique du Saint-Laurent vit en troupeau ?",
        "choix": ["L'orque", "Le beluga", "Le marsouin", "La baleine bleue"],
        "indexBonneReponse": 1,
        "explication": "Le beluga est une baleine blanche endemique du Saint-Laurent.",
    },
    {
        "pavillon": "marin",
        "enonce": "Combien de temps un phoque commun peut-il rester en apnee sous l'eau ?",
        "choix": ["30 secondes", "5 minutes", "15 minutes", "1 heure"],
        "indexBonneReponse": 2,
        "explication": "Le phoque commun plonge en moyenne entre 5 et 15 minutes.",
    },
    {
        "pavillon": "marin",
        "enonce": "Le homard de Gaspesie devient rouge a quel moment ?",
        "choix": ["A la naissance", "Lors de l'accouplement", "A la cuisson", "En hiver"],
        "indexBonneReponse": 2,
        "explication": "Vivant, le homard est brun-vert. Le pigment rouge apparait a la cuisson.",
    },
    {
        "pavillon": "foret",
        "enonce": "Quel est le plus grand cervide d'Amerique du Nord ?",
        "choix": ["Le caribou", "L'orignal", "Le cerf de Virginie", "Le wapiti"],
        "indexBonneReponse": 1,
        "explication": "Un orignal male peut peser plus de 600 kg.",
    },
    {
        "pavillon": "foret",
        "enonce": "Quel arbre porte des fruits rouges en grappes a l'automne dans la foret boreale ?",
        "choix": ["L'erable", "Le sorbier", "L'epinette", "Le bouleau"],
        "indexBonneReponse": 1,
        "explication": "Le sorbier des oiseleurs nourrit les oiseaux migrateurs en automne.",
    },
    {
        "pavillon": "prairie",
        "enonce": "Combien d'ailes possede une abeille ?",
        "choix": ["2", "4", "6", "8"],
        "indexBonneReponse": 1,
        "explication": "L'abeille a deux paires d'ailes, soit quatre ailes au total.",
    },
    {
        "pavillon": "prairie",
        "enonce": "Quelle fleur est essentielle a la reproduction du papillon monarque ?",
        "choix": ["La rose", "L'asclepiade", "Le pissenlit", "Le lys"],
        "indexBonneReponse": 1,
        "explication": "La chenille du monarque ne se nourrit que de feuilles d'asclepiade.",
    },
    {
        "pavillon": "voyageurs",
        "enonce": "Quel oiseau detient le record de la plus longue migration annuelle ?",
        "choix": ["Le harfang des neiges", "La sterne arctique", "Le pygargue", "L'oie des neiges"],
        "indexBonneReponse": 1,
        "explication": "La sterne arctique parcourt plus de 70 000 km par an entre les poles.",
    },
    {
        "pavillon": "voyageurs",
        "enonce": "Pourquoi les bernaches volent-elles en formation en V ?",
        "choix": [
            "Pour faire joli",
            "Pour economiser l'energie",
            "Pour communiquer",
            "Pour suivre le soleil",
        ],
        "indexBonneReponse": 1,
        "explication": "Le V profite des courants ascendants generes par l'oiseau de tete.",
    },
    {
        "pavillon": "voyageurs",
        "enonce": "Quel oiseau pecheur s'identifie a son cri caracteristique sur les lacs ?",
        "choix": ["Le huart", "Le canard colvert", "Le grand heron", "Le cormoran"],
        "indexBonneReponse": 0,
        "explication": "Le huart (plongeon huard) emet un long cri qui porte sur les lacs au crepuscule.",
    },
]


# -----------------------------------------------------------------------------
# Banniere et polices
# -----------------------------------------------------------------------------

def lireBanniereEnvironnement():
    """Lit les variables d'environnement injectees au build (ARG du Dockerfile)."""
    return {
        "buildDate": os.environ.get("BUILD_DATE", "inconnu"),
        "nomEtudiant": os.environ.get("NOM_ETUDIANT", "anonyme"),
        "matricule": os.environ.get("MATRICULE", "000000"),
    }


def chargerPolices():
    """Charge des polices DejaVu installees dans l'image Docker."""
    return {
        "titre": pygame.font.SysFont("dejavusans", 68, bold=True),
        "sousTitre": pygame.font.SysFont("dejavusans", 28, bold=False),
        "question": pygame.font.SysFont("dejavusans", 38, bold=True),
        "choix": pygame.font.SysFont("dejavusans", 30, bold=False),
        "etiquettePavillon": pygame.font.SysFont("dejavusans", 22, bold=True),
        "score": pygame.font.SysFont("dejavusans", 28, bold=True),
        "banniere": pygame.font.SysFont("dejavusans", 18, bold=False),
        "explication": pygame.font.SysFont("dejavusans", 24, bold=False),
    }


# -----------------------------------------------------------------------------
# Helpers texte
# -----------------------------------------------------------------------------

def afficherTexteCentre(surfaceCible, texte, police, couleur, positionY):
    """Dessine un texte centre horizontalement a la position Y donnee."""
    rendu = police.render(texte, True, couleur)
    rectangle = rendu.get_rect(center=(LARGEUR_ECRAN // 2, positionY))
    surfaceCible.blit(rendu, rectangle)
    return rectangle


def afficherTexteEncadre(surfaceCible, texte, police, couleur, positionX, positionY):
    """Dessine un texte aligne a gauche a la position donnee."""
    rendu = police.render(texte, True, couleur)
    surfaceCible.blit(rendu, (positionX, positionY))
    return rendu.get_rect(topleft=(positionX, positionY))


def couperTexteEnLignes(texte, police, largeurMaximum):
    """Decoupe un texte en plusieurs lignes pour qu'il rentre dans la largeur indiquee."""
    mots = texte.split(" ")
    lignes = []
    ligneCourante = ""
    for unMot in mots:
        candidat = (ligneCourante + " " + unMot).strip()
        if police.size(candidat)[0] <= largeurMaximum:
            ligneCourante = candidat
        else:
            if ligneCourante:
                lignes.append(ligneCourante)
            ligneCourante = unMot
    if ligneCourante:
        lignes.append(ligneCourante)
    return lignes


# -----------------------------------------------------------------------------
# Fond degrade + vagues animees (pre-rendus + un rideau d'ondes en surcouche)
# -----------------------------------------------------------------------------

def fabriquerFondDegrade(couleurHaut, couleurBas):
    """Pre-rend un degrade vertical de couleurHaut a couleurBas sur la taille ecran."""
    surfaceFond = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    for positionY in range(HAUTEUR_ECRAN):
        progression = positionY / (HAUTEUR_ECRAN - 1)
        rouge = int(couleurHaut[0] + (couleurBas[0] - couleurHaut[0]) * progression)
        vert = int(couleurHaut[1] + (couleurBas[1] - couleurHaut[1]) * progression)
        bleu = int(couleurHaut[2] + (couleurBas[2] - couleurHaut[2]) * progression)
        pygame.draw.line(surfaceFond, (rouge, vert, bleu), (0, positionY), (LARGEUR_ECRAN, positionY))
    return surfaceFond


def dessinerOndesSurFond(surfaceCible, temps, couleurOnde):
    """Surcouche : 4 sinusoides translucides qui derivent horizontalement."""
    couche = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SRCALPHA)
    for indexOnde in range(4):
        positionYBase = 200 + indexOnde * 130
        amplitude = 14 + indexOnde * 4
        decalagePhase = temps * (0.3 + indexOnde * 0.07) + indexOnde * 1.6
        opacite = 38 - indexOnde * 6
        pointsCourbe = []
        for positionX in range(0, LARGEUR_ECRAN + 12, 12):
            positionY = positionYBase + math.sin(positionX * 0.012 + decalagePhase) * amplitude
            pointsCourbe.append((positionX, positionY))
        if len(pointsCourbe) >= 2:
            pygame.draw.lines(
                couche,
                (*couleurOnde, max(0, opacite)),
                False,
                pointsCourbe,
                2,
            )
    surfaceCible.blit(couche, (0, 0))


# -----------------------------------------------------------------------------
# Decor par pavillon (pre-rendu pour la performance)
# -----------------------------------------------------------------------------

def fabriquerDecorPavillonForet():
    """Arbres + champignons + lievre stylise dans une bande verticale."""
    surface = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SRCALPHA)
    arbres = [
        (90, 280, 28), (60, 380, 22), (140, 460, 32), (90, 560, 26),
        (1140, 280, 30), (1190, 380, 24), (1110, 460, 28), (1170, 560, 26),
    ]
    for positionX, positionY, rayon in arbres:
        pygame.draw.rect(
            surface, (108, 70, 36, 200),
            pygame.Rect(positionX - 5, positionY + rayon - 6, 10, rayon - 4),
            border_radius=2,
        )
        pygame.draw.ellipse(
            surface, (74, 108, 56, 220),
            pygame.Rect(positionX - rayon, positionY - rayon - 6, rayon * 2, rayon * 2 + 8),
        )
        pygame.draw.ellipse(
            surface, (54, 86, 42, 220),
            pygame.Rect(positionX - rayon + 6, positionY - rayon + 4, rayon * 2 - 12, rayon * 2 - 6),
        )
    champignons = [(120, 645), (1170, 650), (40, 670), (1240, 668)]
    for positionX, positionY in champignons:
        pygame.draw.ellipse(
            surface, (200, 70, 70, 220),
            pygame.Rect(positionX - 9, positionY - 7, 18, 12),
        )
        pygame.draw.rect(
            surface, (250, 240, 220, 220),
            pygame.Rect(positionX - 3, positionY + 4, 6, 8),
            border_radius=2,
        )
    return surface


def fabriquerDecorPavillonMarin():
    """Vagues + petits poissons + algues."""
    surface = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SRCALPHA)
    for indexVague in range(8):
        cotePosition = "gauche" if indexVague % 2 == 0 else "droite"
        positionXBase = 60 if cotePosition == "gauche" else LARGEUR_ECRAN - 130
        positionYBase = 240 + indexVague * 50
        for offsetVague in range(2):
            decalageY = offsetVague * 14
            pointsVague = []
            for indexPoint in range(20):
                positionX = positionXBase + indexPoint * 4
                positionY = positionYBase + decalageY + math.sin(indexPoint * 0.6) * 4
                pointsVague.append((positionX, positionY))
            pygame.draw.lines(surface, (255, 255, 255, 200), False, pointsVague, 2)
    poissons = [(100, 600), (1180, 580), (75, 440), (1200, 460)]
    for positionX, positionY in poissons:
        pygame.draw.ellipse(
            surface, (245, 165, 60, 230),
            pygame.Rect(positionX - 12, positionY - 5, 24, 10),
        )
        pygame.draw.polygon(
            surface, (245, 165, 60, 230),
            [
                (positionX + 12, positionY),
                (positionX + 18, positionY - 6),
                (positionX + 18, positionY + 6),
            ],
        )
        pygame.draw.circle(surface, (40, 40, 40, 230), (positionX - 6, positionY - 1), 1)
    algues = [(50, 660), (1230, 660), (95, 670), (1185, 670)]
    for positionX, positionY in algues:
        for indexBrin in range(3):
            decalageBrin = indexBrin * 4 - 4
            pygame.draw.line(
                surface, (60, 110, 90, 220),
                (positionX + decalageBrin, positionY),
                (positionX + decalageBrin + math.sin(indexBrin) * 6, positionY - 22),
                3,
            )
    return surface


def fabriquerDecorPavillonPrairie():
    """Herbes + fleurs colorees + abeilles."""
    surface = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SRCALPHA)
    couleursFleurs = [(232, 82, 140), (251, 207, 61), (169, 107, 212), (255, 138, 80)]
    for indexBrin in range(28):
        positionX = 30 + indexBrin * 18 if indexBrin < 14 else LARGEUR_ECRAN - 270 + (indexBrin - 14) * 18
        if 200 < positionX < LARGEUR_ECRAN - 200:
            continue
        positionY = 660 - (indexBrin % 3) * 6
        pygame.draw.line(surface, (243, 230, 200, 220), (positionX, positionY + 14), (positionX - 8, positionY), 3)
        pygame.draw.line(surface, (243, 230, 200, 220), (positionX, positionY + 14), (positionX + 8, positionY), 3)
        pygame.draw.line(surface, (243, 230, 200, 220), (positionX, positionY + 14), (positionX, positionY - 4), 3)
    fleurs = [
        (60, 600), (110, 580), (160, 605), (1120, 590), (1180, 575), (1240, 600),
        (40, 510), (1240, 510), (90, 460), (1190, 460),
    ]
    for indexFleur, (positionX, positionY) in enumerate(fleurs):
        couleur = couleursFleurs[indexFleur % len(couleursFleurs)]
        for offsetX, offsetY in [(0, -4), (-4, -1), (4, -1), (-2, 3), (2, 3)]:
            pygame.draw.circle(surface, (*couleur, 230), (positionX + offsetX, positionY + offsetY), 4)
        pygame.draw.circle(surface, (255, 244, 173, 240), (positionX, positionY), 2)
        pygame.draw.line(surface, (63, 122, 43, 220), (positionX, positionY + 5), (positionX, positionY + 14), 2)
    abeilles = [(140, 380), (1130, 360), (60, 320), (1230, 330)]
    for positionX, positionY in abeilles:
        pygame.draw.ellipse(surface, (255, 255, 255, 220), pygame.Rect(positionX - 5, positionY - 5, 7, 4))
        pygame.draw.ellipse(surface, (255, 255, 255, 220), pygame.Rect(positionX - 1, positionY - 5, 7, 4))
        pygame.draw.ellipse(surface, (251, 207, 61, 240), pygame.Rect(positionX - 5, positionY - 2, 10, 6))
        pygame.draw.line(surface, (40, 40, 40, 240), (positionX - 2, positionY - 2), (positionX - 2, positionY + 3), 1)
        pygame.draw.line(surface, (40, 40, 40, 240), (positionX + 1, positionY - 2), (positionX + 1, positionY + 3), 1)
    return surface


def fabriquerDecorPavillonVoyageurs():
    """Oiseaux en formation V + nuages discrets."""
    surface = pygame.Surface((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SRCALPHA)
    formations = [
        (180, 250), (1100, 320), (220, 480), (1080, 540),
    ]
    for positionXTete, positionYTete in formations:
        for indexOiseau in range(5):
            decalageX = indexOiseau * 22
            decalageY = indexOiseau * 14
            for cotePosition in (-1, 1):
                positionXOiseau = positionXTete + cotePosition * decalageX
                positionYOiseau = positionYTete + decalageY
                pygame.draw.lines(
                    surface, (60, 50, 40, 220), False,
                    [
                        (positionXOiseau - 6, positionYOiseau + 3),
                        (positionXOiseau - 2, positionYOiseau - 2),
                        (positionXOiseau + 2, positionYOiseau - 2),
                        (positionXOiseau + 6, positionYOiseau + 3),
                    ],
                    2,
                )
                if indexOiseau == 0 and cotePosition == 1:
                    break
    nuages = [(110, 200, 60), (1170, 240, 70), (90, 380, 50), (1190, 410, 55)]
    for positionX, positionY, largeurNuage in nuages:
        pygame.draw.ellipse(
            surface, (255, 253, 246, 220),
            pygame.Rect(positionX - largeurNuage // 2, positionY - 12, largeurNuage, 24),
        )
        pygame.draw.ellipse(
            surface, (255, 253, 246, 220),
            pygame.Rect(positionX - largeurNuage // 2 - 12, positionY - 6, largeurNuage // 2, 14),
        )
        pygame.draw.ellipse(
            surface, (255, 253, 246, 220),
            pygame.Rect(positionX + largeurNuage // 4, positionY - 8, largeurNuage // 2, 16),
        )
    return surface


# -----------------------------------------------------------------------------
# Etincelles (animation sur bonne reponse)
# -----------------------------------------------------------------------------

class Etincelle:
    """Particule qui jaillit du centre d'une bonne reponse, retombe et s'efface."""

    def __init__(self, positionX, positionY, couleur):
        angleEjection = random.uniform(-math.pi, 0)
        vitesseEjection = random.uniform(220, 420)
        self.positionX = float(positionX)
        self.positionY = float(positionY)
        self.vitesseX = math.cos(angleEjection) * vitesseEjection
        self.vitesseY = math.sin(angleEjection) * vitesseEjection
        self.dureeVie = random.uniform(0.7, 1.3)
        self.tempsRestant = self.dureeVie
        self.rayon = random.uniform(2.5, 5.0)
        self.couleur = couleur

    def mettreAJour(self, deltaTemps):
        self.tempsRestant -= deltaTemps
        self.positionX += self.vitesseX * deltaTemps
        self.positionY += self.vitesseY * deltaTemps
        self.vitesseY += 720 * deltaTemps
        self.vitesseX *= 0.985

    def estVivante(self):
        return self.tempsRestant > 0

    def dessiner(self, surfaceCible):
        opaciteRelative = max(0.0, self.tempsRestant / self.dureeVie)
        rayonAffiche = max(1.0, self.rayon * (0.4 + opaciteRelative * 0.6))
        couche = pygame.Surface(
            (int(rayonAffiche * 2 + 4), int(rayonAffiche * 2 + 4)), pygame.SRCALPHA
        )
        pygame.draw.circle(
            couche,
            (*self.couleur, int(opaciteRelative * 255)),
            (int(rayonAffiche + 2), int(rayonAffiche + 2)),
            int(rayonAffiche),
        )
        surfaceCible.blit(
            couche,
            (int(self.positionX - rayonAffiche - 2), int(self.positionY - rayonAffiche - 2)),
        )


# -----------------------------------------------------------------------------
# Mascotte beluga + bulle de dialogue
# -----------------------------------------------------------------------------

def dessinerMascotteBeluga(surfaceCible, positionX, positionY, expression, temps, echelle=1.0):
    """
    Dessine la mascotte beluga centree sur (positionX, positionY).
    expression: 'neutre', 'content', 'desole'.
    echelle : 1.0 = 220x180 px sur surface, valeurs plus petites pour reduire.
    Le beluga bobe verticalement avec le temps pour donner vie au personnage.
    """
    decalageBobbing = math.sin(temps * 1.8) * 6
    centreX = positionX
    centreY = positionY + decalageBobbing

    couche = pygame.Surface((220, 180), pygame.SRCALPHA)
    decalageOrigineX = 110
    decalageOrigineY = 90

    pygame.draw.ellipse(
        couche,
        (0, 0, 0, 50),
        pygame.Rect(decalageOrigineX - 60, decalageOrigineY + 50, 120, 18),
    )

    pygame.draw.ellipse(
        couche, COULEUR_MASCOTTE_OMBRE,
        pygame.Rect(decalageOrigineX - 56, decalageOrigineY - 32, 110, 70),
    )
    pygame.draw.ellipse(
        couche, COULEUR_MASCOTTE_CORPS,
        pygame.Rect(decalageOrigineX - 60, decalageOrigineY - 36, 110, 68),
    )

    pygame.draw.polygon(
        couche, COULEUR_MASCOTTE_CORPS,
        [
            (decalageOrigineX + 50, decalageOrigineY),
            (decalageOrigineX + 90, decalageOrigineY - 22),
            (decalageOrigineX + 90, decalageOrigineY + 22),
        ],
    )
    pygame.draw.polygon(
        couche, COULEUR_MASCOTTE_TRAIT,
        [
            (decalageOrigineX + 50, decalageOrigineY),
            (decalageOrigineX + 90, decalageOrigineY - 22),
            (decalageOrigineX + 90, decalageOrigineY + 22),
        ],
        width=2,
    )

    pygame.draw.ellipse(
        couche, COULEUR_MASCOTTE_OMBRE,
        pygame.Rect(decalageOrigineX - 78, decalageOrigineY - 22, 36, 28),
    )
    pygame.draw.ellipse(
        couche, COULEUR_MASCOTTE_CORPS,
        pygame.Rect(decalageOrigineX - 80, decalageOrigineY - 26, 36, 26),
    )

    pygame.draw.ellipse(
        couche, COULEUR_MASCOTTE_TRAIT,
        pygame.Rect(decalageOrigineX - 60, decalageOrigineY - 36, 110, 68),
        width=2,
    )
    pygame.draw.ellipse(
        couche, COULEUR_MASCOTTE_TRAIT,
        pygame.Rect(decalageOrigineX - 80, decalageOrigineY - 26, 36, 26),
        width=2,
    )

    rectangleNageoire = pygame.Rect(decalageOrigineX - 18, decalageOrigineY + 14, 32, 18)
    pygame.draw.ellipse(couche, COULEUR_MASCOTTE_OMBRE, rectangleNageoire)
    pygame.draw.ellipse(couche, COULEUR_MASCOTTE_TRAIT, rectangleNageoire, width=2)

    pygame.draw.circle(
        couche, COULEUR_MASCOTTE_TRAIT,
        (decalageOrigineX - 56, decalageOrigineY - 14),
        4,
    )
    pygame.draw.circle(
        couche, (255, 255, 255),
        (decalageOrigineX - 55, decalageOrigineY - 15),
        1,
    )

    if expression == "content":
        pygame.draw.arc(
            couche, COULEUR_MASCOTTE_TRAIT,
            pygame.Rect(decalageOrigineX - 70, decalageOrigineY - 8, 22, 18),
            math.pi, 2 * math.pi, 3,
        )
    elif expression == "desole":
        pygame.draw.arc(
            couche, COULEUR_MASCOTTE_TRAIT,
            pygame.Rect(decalageOrigineX - 70, decalageOrigineY - 4, 22, 14),
            0.2, math.pi - 0.2, 3,
        )
    else:
        pygame.draw.line(
            couche, COULEUR_MASCOTTE_TRAIT,
            (decalageOrigineX - 68, decalageOrigineY + 2),
            (decalageOrigineX - 50, decalageOrigineY + 2),
            3,
        )

    if echelle != 1.0:
        nouvelleLargeur = max(1, int(220 * echelle))
        nouvelleHauteur = max(1, int(180 * echelle))
        couche = pygame.transform.smoothscale(couche, (nouvelleLargeur, nouvelleHauteur))
        decalageOrigineX = int(decalageOrigineX * echelle)
        decalageOrigineY = int(decalageOrigineY * echelle)

    surfaceCible.blit(
        couche,
        (int(centreX - decalageOrigineX), int(centreY - decalageOrigineY)),
    )


def dessinerBulleDialogue(surfaceCible, police, texte, ancrageX, ancrageY):
    """
    Dessine une bulle de dialogue avec contour noir, texte centre,
    et un petit triangle pointant vers (ancrageX, ancrageY) (direction de la mascotte).
    La bulle apparait au-dessus et a gauche du point d'ancrage.
    """
    if not texte:
        return
    rendu = police.render(texte, True, COULEUR_TEXTE_PRINCIPAL)
    margesBulle = 18
    largeurBulle = rendu.get_width() + margesBulle * 2
    hauteurBulle = rendu.get_height() + margesBulle * 2

    positionXBulle = ancrageX - largeurBulle - 10
    positionYBulle = ancrageY - hauteurBulle - 10
    rectangleBulle = pygame.Rect(positionXBulle, positionYBulle, largeurBulle, hauteurBulle)

    pygame.draw.rect(surfaceCible, COULEUR_BULLE_FOND, rectangleBulle, border_radius=14)
    pygame.draw.rect(surfaceCible, COULEUR_BULLE_CONTOUR, rectangleBulle, width=3, border_radius=14)
    surfaceCible.blit(
        rendu,
        (positionXBulle + margesBulle, positionYBulle + margesBulle),
    )

    pointeTriangle = [
        (rectangleBulle.right - 30, rectangleBulle.bottom),
        (rectangleBulle.right - 6, rectangleBulle.bottom),
        (rectangleBulle.right + 4, rectangleBulle.bottom + 18),
    ]
    pygame.draw.polygon(surfaceCible, COULEUR_BULLE_FOND, pointeTriangle)
    pygame.draw.line(
        surfaceCible, COULEUR_BULLE_CONTOUR,
        pointeTriangle[0], pointeTriangle[2], 3,
    )
    pygame.draw.line(
        surfaceCible, COULEUR_BULLE_CONTOUR,
        pointeTriangle[1], pointeTriangle[2], 3,
    )


# -----------------------------------------------------------------------------
# Banniere
# -----------------------------------------------------------------------------

def dessinerBanniere(surfaceCible, polices, banniere):
    """Banniere d'identification de la borne en haut de l'ecran."""
    hauteurBanniere = 40
    pygame.draw.rect(surfaceCible, COULEUR_BANNIERE, pygame.Rect(0, 0, LARGEUR_ECRAN, hauteurBanniere))
    texteGauche = "Borne medias - Quiz du Zoo maritime du Bas-Saint-Laurent"
    texteDroite = (
        f"{banniere['nomEtudiant']} - {banniere['matricule']} - build {banniere['buildDate']}"
    )
    afficherTexteEncadre(surfaceCible, texteGauche, polices["banniere"], COULEUR_TEXTE_INVERSE, 18, 10)
    largeurDroite = polices["banniere"].size(texteDroite)[0]
    afficherTexteEncadre(
        surfaceCible, texteDroite, polices["banniere"], COULEUR_TEXTE_INVERSE,
        LARGEUR_ECRAN - largeurDroite - 18, 10,
    )


# -----------------------------------------------------------------------------
# Carte de question avec ombre douce + bandeau colore
# -----------------------------------------------------------------------------

CARTE_LARGEUR = 1000
CARTE_HAUTEUR = 540
CARTE_POSITION_X = (LARGEUR_ECRAN - CARTE_LARGEUR) // 2
CARTE_POSITION_Y = 90


def dessinerCarteQuestion(surfaceCible, couleurAccentPavillon):
    """Carte centrale : ombre douce + contour noir + bandeau pavillon a gauche."""
    surfaceOmbre = pygame.Surface((CARTE_LARGEUR + 28, CARTE_HAUTEUR + 28), pygame.SRCALPHA)
    for indexCouche in range(10):
        decalage = indexCouche * 2
        opacite = 18 - indexCouche
        pygame.draw.rect(
            surfaceOmbre,
            (0, 0, 0, max(0, opacite)),
            pygame.Rect(decalage, decalage, CARTE_LARGEUR + 28 - decalage * 2, CARTE_HAUTEUR + 28 - decalage * 2),
            border_radius=22,
        )
    surfaceCible.blit(surfaceOmbre, (CARTE_POSITION_X - 14, CARTE_POSITION_Y - 6))

    rectangleCarte = pygame.Rect(CARTE_POSITION_X, CARTE_POSITION_Y, CARTE_LARGEUR, CARTE_HAUTEUR)
    pygame.draw.rect(surfaceCible, COULEUR_CARTE, rectangleCarte, border_radius=18)

    pygame.draw.rect(
        surfaceCible,
        couleurAccentPavillon,
        pygame.Rect(CARTE_POSITION_X, CARTE_POSITION_Y, 14, CARTE_HAUTEUR),
        border_top_left_radius=18,
        border_bottom_left_radius=18,
    )

    pygame.draw.rect(
        surfaceCible,
        COULEUR_CARTE_CONTOUR,
        rectangleCarte,
        width=4,
        border_radius=18,
    )


def calculerRectanglesChoix():
    """Quatre rectangles pour les reponses, dans la carte."""
    largeur = 440
    hauteur = 86
    espace = 18
    positionXGauche = CARTE_POSITION_X + 50
    positionXDroite = positionXGauche + largeur + espace
    positionYHaute = CARTE_POSITION_Y + 290
    positionYBasse = positionYHaute + hauteur + espace
    return [
        pygame.Rect(positionXGauche, positionYHaute, largeur, hauteur),
        pygame.Rect(positionXDroite, positionYHaute, largeur, hauteur),
        pygame.Rect(positionXGauche, positionYBasse, largeur, hauteur),
        pygame.Rect(positionXDroite, positionYBasse, largeur, hauteur),
    ]


# -----------------------------------------------------------------------------
# Ecrans
# -----------------------------------------------------------------------------

def dessinerEcranAccueil(surfaceCible, fondPrerendu, polices, banniere, temps):
    surfaceCible.blit(fondPrerendu["accueil"], (0, 0))
    dessinerOndesSurFond(surfaceCible, temps, (130, 110, 80))
    dessinerBanniere(surfaceCible, polices, banniere)

    afficherTexteCentre(surfaceCible, "Quiz des especes", polices["titre"], COULEUR_TEXTE_PRINCIPAL, 180)
    afficherTexteCentre(
        surfaceCible,
        "Decouvre la faune et la flore du Saint-Laurent",
        polices["sousTitre"],
        COULEUR_TEXTE_DOUX,
        260,
    )
    afficherTexteCentre(
        surfaceCible,
        f"{len(QUESTIONS)} questions reparties dans les quatre pavillons",
        polices["sousTitre"],
        COULEUR_TEXTE_DOUX,
        306,
    )

    largeurAction = 480
    rectangleAction = pygame.Rect(
        (LARGEUR_ECRAN - largeurAction) // 2, 360, largeurAction, 86,
    )
    pygame.draw.rect(surfaceCible, COULEUR_ACCENT, rectangleAction, border_radius=18)
    pygame.draw.rect(
        surfaceCible, COULEUR_CARTE_CONTOUR, rectangleAction, width=3, border_radius=18,
    )
    afficherTexteCentre(
        surfaceCible,
        "Touche ESPACE ou clic pour commencer",
        polices["choix"],
        COULEUR_TEXTE_INVERSE,
        rectangleAction.centery,
    )

    centreMascotteX = LARGEUR_ECRAN // 2
    centreMascotteY = HAUTEUR_ECRAN - 110
    dessinerMascotteBeluga(
        surfaceCible, centreMascotteX, centreMascotteY,
        "content", temps, echelle=0.85,
    )
    dessinerBulleDialogue(
        surfaceCible, polices["score"], "Salut !",
        centreMascotteX - 80, centreMascotteY - 60,
    )

    afficherTexteCentre(
        surfaceCible,
        "ESC pour quitter - touches 1 a 4 ou clic pour repondre",
        polices["banniere"],
        COULEUR_TEXTE_DOUX,
        HAUTEUR_ECRAN - 30,
    )


def dessinerEcranQuestion(
    surfaceCible,
    fondPrerendu,
    decorsPavillon,
    polices,
    banniere,
    question,
    indexQuestion,
    rectanglesChoix,
    positionSouris,
    indexChoixUtilisateur,
    temps,
):
    pavillonCle = question["pavillon"]
    surfaceCible.blit(fondPrerendu[pavillonCle], (0, 0))
    dessinerOndesSurFond(surfaceCible, temps, COULEURS_PAVILLON[pavillonCle])
    surfaceCible.blit(decorsPavillon[pavillonCle], (0, 0))
    dessinerBanniere(surfaceCible, polices, banniere)

    couleurAccent = COULEURS_PAVILLON[pavillonCle]
    dessinerCarteQuestion(surfaceCible, couleurAccent)

    afficherTexteEncadre(
        surfaceCible,
        f"Question {indexQuestion + 1} / {len(QUESTIONS)}",
        polices["score"],
        couleurAccent,
        CARTE_POSITION_X + 36,
        CARTE_POSITION_Y + 26,
    )

    rendu_etiquette_pavillon = polices["etiquettePavillon"].render(
        NOMS_PAVILLON[pavillonCle].upper(), True, COULEUR_TEXTE_PRINCIPAL,
    )
    rectangle_surlignement = pygame.Rect(
        CARTE_POSITION_X + 30,
        CARTE_POSITION_Y + 68,
        rendu_etiquette_pavillon.get_width() + 18,
        rendu_etiquette_pavillon.get_height() + 6,
    )
    pygame.draw.rect(
        surfaceCible, COULEUR_SURLIGNEMENT, rectangle_surlignement, border_radius=4,
    )
    surfaceCible.blit(
        rendu_etiquette_pavillon,
        (CARTE_POSITION_X + 39, CARTE_POSITION_Y + 70),
    )

    pygame.draw.line(
        surfaceCible,
        couleurAccent,
        (CARTE_POSITION_X + 36, CARTE_POSITION_Y + 112),
        (CARTE_POSITION_X + CARTE_LARGEUR - 36, CARTE_POSITION_Y + 112),
        3,
    )

    lignesEnonce = couperTexteEnLignes(
        question["enonce"], polices["question"], CARTE_LARGEUR - 120
    )
    positionYTexte = CARTE_POSITION_Y + 150
    for uneLigne in lignesEnonce:
        rendu = polices["question"].render(uneLigne, True, couleurAccent)
        rectangleTexte = rendu.get_rect(midtop=(LARGEUR_ECRAN // 2, positionYTexte))
        surfaceCible.blit(rendu, rectangleTexte)
        positionYTexte += 48

    for indexChoix, unRectangle in enumerate(rectanglesChoix):
        couleurFond = COULEUR_REPONSE_FOND
        couleurBordure = COULEUR_REPONSE_BORDURE
        couleurTexte = COULEUR_TEXTE_PRINCIPAL
        if indexChoixUtilisateur is not None:
            if indexChoix == question["indexBonneReponse"]:
                couleurFond = COULEUR_REPONSE_BONNE
                couleurBordure = COULEUR_REPONSE_BONNE
                couleurTexte = COULEUR_TEXTE_INVERSE
            elif indexChoix == indexChoixUtilisateur:
                couleurFond = COULEUR_REPONSE_MAUVAISE
                couleurBordure = COULEUR_REPONSE_MAUVAISE
                couleurTexte = COULEUR_TEXTE_INVERSE
        elif unRectangle.collidepoint(positionSouris):
            couleurFond = COULEUR_REPONSE_SURVOL
            couleurBordure = couleurAccent

        pygame.draw.rect(surfaceCible, couleurFond, unRectangle, border_radius=14)
        pygame.draw.rect(surfaceCible, couleurBordure, unRectangle, width=3, border_radius=14)
        rendu = polices["choix"].render(
            f"{indexChoix + 1}.  {question['choix'][indexChoix]}", True, couleurTexte
        )
        rectangleTexte = rendu.get_rect(center=unRectangle.center)
        surfaceCible.blit(rendu, rectangleTexte)

    if indexChoixUtilisateur is not None:
        positionYExplication = CARTE_POSITION_Y + CARTE_HAUTEUR + 16
        lignesExplication = couperTexteEnLignes(
            question["explication"], polices["explication"], LARGEUR_ECRAN - 200
        )
        for uneLigne in lignesExplication:
            afficherTexteCentre(
                surfaceCible, uneLigne, polices["explication"],
                COULEUR_TEXTE_PRINCIPAL, positionYExplication,
            )
            positionYExplication += 30
        afficherTexteCentre(
            surfaceCible,
            "Touche ESPACE pour la suite",
            polices["banniere"],
            COULEUR_TEXTE_DOUX,
            HAUTEUR_ECRAN - 24,
        )

    if indexChoixUtilisateur is None:
        expressionMascotte = "neutre"
    elif indexChoixUtilisateur == question["indexBonneReponse"]:
        expressionMascotte = "content"
    else:
        expressionMascotte = "desole"

    centreMascotteX = LARGEUR_ECRAN - 75
    centreMascotteY = CARTE_POSITION_Y + 200
    dessinerMascotteBeluga(
        surfaceCible, centreMascotteX, centreMascotteY,
        expressionMascotte, temps, echelle=0.55,
    )


def dessinerEcranFinal(surfaceCible, fondPrerendu, polices, banniere, score, total, temps):
    surfaceCible.blit(fondPrerendu["accueil"], (0, 0))
    dessinerOndesSurFond(surfaceCible, temps, (130, 110, 80))
    dessinerBanniere(surfaceCible, polices, banniere)

    afficherTexteCentre(surfaceCible, "Quiz termine", polices["titre"], COULEUR_TEXTE_PRINCIPAL, 180)
    afficherTexteCentre(
        surfaceCible, f"Score : {score} / {total}", polices["question"],
        COULEUR_ACCENT, 270,
    )

    if score == total:
        message = "Bravo, tu connais bien le Saint-Laurent !"
        bulleMascotte = "Parfait !"
        expressionMascotte = "content"
    elif score >= total * 0.7:
        message = "Tres bien, le zoo n'a presque plus de secrets pour toi."
        bulleMascotte = "Bien joue !"
        expressionMascotte = "content"
    elif score >= total * 0.4:
        message = "Pas mal - reviens visiter les pavillons pour en apprendre davantage."
        bulleMascotte = "Pas mal !"
        expressionMascotte = "neutre"
    else:
        message = "Une visite des pavillons s'impose pour decouvrir nos especes."
        bulleMascotte = "A bientot !"
        expressionMascotte = "desole"
    afficherTexteCentre(surfaceCible, message, polices["sousTitre"], COULEUR_TEXTE_DOUX, 320)

    largeurAction = 480
    rectangleAction = pygame.Rect((LARGEUR_ECRAN - largeurAction) // 2, 360, largeurAction, 80)
    pygame.draw.rect(surfaceCible, COULEUR_ACCENT, rectangleAction, border_radius=18)
    pygame.draw.rect(
        surfaceCible, COULEUR_CARTE_CONTOUR, rectangleAction, width=3, border_radius=18,
    )
    afficherTexteCentre(
        surfaceCible,
        "ESPACE pour rejouer - ESC pour fermer",
        polices["choix"],
        COULEUR_TEXTE_INVERSE,
        rectangleAction.centery,
    )

    centreMascotteX = LARGEUR_ECRAN // 2
    centreMascotteY = HAUTEUR_ECRAN - 110
    dessinerMascotteBeluga(
        surfaceCible, centreMascotteX, centreMascotteY,
        expressionMascotte, temps, echelle=0.85,
    )
    dessinerBulleDialogue(
        surfaceCible, polices["score"], bulleMascotte,
        centreMascotteX - 80, centreMascotteY - 60,
    )


# -----------------------------------------------------------------------------
# Logique de partie
# -----------------------------------------------------------------------------

def melangerQuestions():
    """Retourne une copie melangee des questions pour eviter l'ordre fige."""
    copie = list(QUESTIONS)
    random.shuffle(copie)
    return copie


def emettreEtincelles(rectangle, couleur):
    """Cree une volee de particules au centre du rectangle gagnant."""
    centre = rectangle.center
    return [Etincelle(centre[0], centre[1], couleur) for _ in range(36)]


def boucleBorne():
    pygame.init()
    surfaceEcran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.set_caption("Borne medias - Quiz du zoo maritime")
    horloge = pygame.time.Clock()

    polices = chargerPolices()
    banniere = lireBanniereEnvironnement()
    rectanglesChoix = calculerRectanglesChoix()

    fondPrerendu = {
        "accueil": fabriquerFondDegrade(COULEUR_FOND_HAUT, COULEUR_FOND_BAS),
    }
    for clePavillon, couleurDouce in COULEURS_PAVILLON_DOUX.items():
        fondPrerendu[clePavillon] = fabriquerFondDegrade(couleurDouce, COULEUR_FOND_BAS)

    decorsPavillon = {
        "foret": fabriquerDecorPavillonForet(),
        "marin": fabriquerDecorPavillonMarin(),
        "prairie": fabriquerDecorPavillonPrairie(),
        "voyageurs": fabriquerDecorPavillonVoyageurs(),
    }

    etatCourant = "accueil"
    questionsActives = melangerQuestions()
    indexQuestion = 0
    indexChoixUtilisateur = None
    score = 0
    etincelles = []
    tempsTotal = 0.0

    def repondre(indexChoix):
        """Centralise le traitement d'une reponse (clavier ou clic)."""
        nonlocal indexChoixUtilisateur, score, etincelles
        if indexChoixUtilisateur is not None:
            return
        indexChoixUtilisateur = indexChoix
        questionCourante = questionsActives[indexQuestion]
        if indexChoix == questionCourante["indexBonneReponse"]:
            score += 1
            rectangleGagnant = rectanglesChoix[indexChoix]
            etincelles.extend(
                emettreEtincelles(rectangleGagnant, COULEUR_REPONSE_BONNE)
            )

    def passerQuestionSuivante():
        nonlocal indexQuestion, indexChoixUtilisateur, etatCourant, etincelles
        indexQuestion += 1
        indexChoixUtilisateur = None
        etincelles = []
        if indexQuestion >= len(questionsActives):
            etatCourant = "final"

    def demarrerNouvellePartie():
        nonlocal etatCourant, questionsActives, indexQuestion, indexChoixUtilisateur, score, etincelles
        etatCourant = "question"
        questionsActives = melangerQuestions()
        indexQuestion = 0
        indexChoixUtilisateur = None
        score = 0
        etincelles = []

    while True:
        deltaTemps = horloge.tick(60) / 1000.0
        tempsTotal += deltaTemps

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                return
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if etatCourant == "accueil" and evenement.key == pygame.K_SPACE:
                    demarrerNouvellePartie()
                elif etatCourant == "question":
                    if indexChoixUtilisateur is None:
                        for indexTouche, codeTouche in enumerate(
                            [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
                        ):
                            if evenement.key == codeTouche:
                                repondre(indexTouche)
                                break
                    elif evenement.key == pygame.K_SPACE:
                        passerQuestionSuivante()
                elif etatCourant == "final" and evenement.key == pygame.K_SPACE:
                    etatCourant = "accueil"
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                if etatCourant == "accueil":
                    demarrerNouvellePartie()
                elif etatCourant == "question":
                    if indexChoixUtilisateur is None:
                        for indexChoix, unRectangle in enumerate(rectanglesChoix):
                            if unRectangle.collidepoint(evenement.pos):
                                repondre(indexChoix)
                                break
                    else:
                        passerQuestionSuivante()
                elif etatCourant == "final":
                    etatCourant = "accueil"

        positionSouris = pygame.mouse.get_pos()

        if etatCourant == "accueil":
            dessinerEcranAccueil(surfaceEcran, fondPrerendu, polices, banniere, tempsTotal)
        elif etatCourant == "question":
            dessinerEcranQuestion(
                surfaceEcran, fondPrerendu, decorsPavillon, polices, banniere,
                questionsActives[indexQuestion], indexQuestion, rectanglesChoix,
                positionSouris, indexChoixUtilisateur, tempsTotal,
            )
        elif etatCourant == "final":
            dessinerEcranFinal(
                surfaceEcran, fondPrerendu, polices, banniere, score,
                len(questionsActives), tempsTotal,
            )

        for uneEtincelle in etincelles:
            uneEtincelle.mettreAJour(deltaTemps)
            uneEtincelle.dessiner(surfaceEcran)
        etincelles = [uneEtincelle for uneEtincelle in etincelles if uneEtincelle.estVivante()]

        pygame.display.flip()


if __name__ == "__main__":
    try:
        boucleBorne()
    except pygame.error as erreur:
        print(
            "Pygame n'a pas pu demarrer. Verifie que DISPLAY est partage avec le container.\n"
            f"Detail : {erreur}",
            file=sys.stderr,
        )
        sys.exit(1)
