"""
Borne intelligente vision - identification d'animaux par modele ONNX local.
Zoo maritime du Bas-Saint-Laurent.

Application kiosque Pygame qui affiche une grille de photos d'animaux.
Au clic sur une vignette, l'image est passee a un modele MobileNetV2
charge localement via onnxruntime, et les top-3 predictions sont affichees
sous forme de barres horizontales.

Aucun appel reseau au runtime : modele et labels sont dans l'image Docker.
"""

import os
import sys

import pygame

from classifieur import classifierImage, initialiserClassifieur

LARGEUR_ECRAN = 1280
HAUTEUR_ECRAN = 720

REPERTOIRE_PHOTOS = "/borne/photos"

# ----- Palette -----
COULEUR_FOND_HAUT = (250, 244, 226)
COULEUR_FOND_BAS = (236, 224, 196)
COULEUR_TEXTE_PRINCIPAL = (40, 40, 42)
COULEUR_TEXTE_DOUX = (98, 96, 88)
COULEUR_TEXTE_INVERSE = (255, 253, 246)
COULEUR_BANNIERE = (31, 77, 44)
COULEUR_CARTE = (255, 253, 246)
COULEUR_VIGNETTE_BORDURE = (210, 200, 175)
COULEUR_VIGNETTE_SURVOL = (39, 174, 96)
COULEUR_BARRE_FOND = (228, 220, 198)
COULEUR_BARRE_PLEINE = (39, 174, 96)
COULEUR_ACCENT = (210, 48, 48)


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
        "titre": pygame.font.SysFont("dejavusans", 48, bold=True),
        "sousTitre": pygame.font.SysFont("dejavusans", 26, bold=False),
        "vignette": pygame.font.SysFont("dejavusans", 18, bold=False),
        "resultatTitre": pygame.font.SysFont("dejavusans", 30, bold=True),
        "resultatLigne": pygame.font.SysFont("dejavusans", 22, bold=False),
        "resultatProba": pygame.font.SysFont("dejavusans", 22, bold=True),
        "action": pygame.font.SysFont("dejavusans", 24, bold=True),
        "banniere": pygame.font.SysFont("dejavusans", 18, bold=False),
        "info": pygame.font.SysFont("dejavusans", 20, bold=False),
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


# -----------------------------------------------------------------------------
# Banniere d'identification
# -----------------------------------------------------------------------------

def dessinerBanniere(surfaceCible, polices, banniere):
    """Banniere d'identification de la borne en haut de l'ecran."""
    hauteurBanniere = 40
    pygame.draw.rect(surfaceCible, COULEUR_BANNIERE, pygame.Rect(0, 0, LARGEUR_ECRAN, hauteurBanniere))
    texteGauche = "Borne intelligente vision - Zoo maritime du Bas-Saint-Laurent"
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
# Fond degrade
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


# -----------------------------------------------------------------------------
# Chargement des photos disponibles
# -----------------------------------------------------------------------------

def listerPhotosDisponibles(repertoire):
    """Retourne la liste triee des chemins de photos jpeg dans le repertoire donne."""
    if not os.path.isdir(repertoire):
        return []
    fichiersTries = sorted(os.listdir(repertoire))
    cheminsPhotos = []
    for unNomFichier in fichiersTries:
        extensionMinuscule = os.path.splitext(unNomFichier)[1].lower()
        if extensionMinuscule in (".jpg", ".jpeg", ".png"):
            cheminsPhotos.append(os.path.join(repertoire, unNomFichier))
    return cheminsPhotos


def chargerVignettes(cheminsPhotos, largeurVignette, hauteurVignette):
    """Charge chaque photo, la met a l'echelle pour la galerie et garde aussi une version 500x500 pour l'ecran resultat."""
    vignettes = []
    for unChemin in cheminsPhotos:
        try:
            surfaceImage = pygame.image.load(unChemin).convert()
        except pygame.error:
            continue
        surfaceVignette = pygame.transform.smoothscale(
            surfaceImage, (largeurVignette, hauteurVignette)
        )
        # Version agrandie pour l'ecran resultat (max 500x500, ratio preserve).
        largeurOriginale, hauteurOriginale = surfaceImage.get_size()
        facteurEchelle = min(500 / largeurOriginale, 500 / hauteurOriginale)
        largeurAgrandie = max(1, int(largeurOriginale * facteurEchelle))
        hauteurAgrandie = max(1, int(hauteurOriginale * facteurEchelle))
        surfaceAgrandie = pygame.transform.smoothscale(
            surfaceImage, (largeurAgrandie, hauteurAgrandie)
        )
        vignettes.append({
            "chemin": unChemin,
            "nomFichier": os.path.basename(unChemin),
            "surfaceVignette": surfaceVignette,
            "surfaceAgrandie": surfaceAgrandie,
        })
    return vignettes


def calculerRectanglesVignettes(nombreVignettes, largeurVignette, hauteurVignette):
    """Calcule les rectangles d'une grille 3x3 (max) centree sous la banniere."""
    nombreColonnes = 3
    espaceHorizontal = 30
    espaceVertical = 50
    largeurGrille = nombreColonnes * largeurVignette + (nombreColonnes - 1) * espaceHorizontal
    positionXGauche = (LARGEUR_ECRAN - largeurGrille) // 2
    positionYHaut = 130
    rectangles = []
    for indexCourant in range(nombreVignettes):
        colonneCourante = indexCourant % nombreColonnes
        ligneCourante = indexCourant // nombreColonnes
        positionX = positionXGauche + colonneCourante * (largeurVignette + espaceHorizontal)
        positionY = positionYHaut + ligneCourante * (hauteurVignette + espaceVertical)
        rectangles.append(pygame.Rect(positionX, positionY, largeurVignette, hauteurVignette))
    return rectangles


# -----------------------------------------------------------------------------
# Ecrans
# -----------------------------------------------------------------------------

def dessinerEcranGalerie(
    surfaceCible, fondPrerendu, polices, banniere, vignettes, rectanglesVignettes, positionSouris
):
    surfaceCible.blit(fondPrerendu, (0, 0))
    dessinerBanniere(surfaceCible, polices, banniere)

    afficherTexteCentre(
        surfaceCible,
        "Touche une photo pour identifier l'animal",
        polices["titre"],
        COULEUR_TEXTE_PRINCIPAL,
        80,
    )

    for indexVignette, uneVignette in enumerate(vignettes):
        rectangleVignette = rectanglesVignettes[indexVignette]
        # Cadre clair derriere la vignette pour un effet "carte".
        rectangleCadre = rectangleVignette.inflate(16, 38)
        rectangleCadre.move_ip(0, 8)
        pygame.draw.rect(surfaceCible, COULEUR_CARTE, rectangleCadre, border_radius=12)

        couleurBordure = COULEUR_VIGNETTE_BORDURE
        epaisseurBordure = 2
        if rectangleCadre.collidepoint(positionSouris):
            couleurBordure = COULEUR_VIGNETTE_SURVOL
            epaisseurBordure = 4
        pygame.draw.rect(surfaceCible, couleurBordure, rectangleCadre, width=epaisseurBordure, border_radius=12)

        surfaceCible.blit(uneVignette["surfaceVignette"], rectangleVignette.topleft)

        rendu = polices["vignette"].render(
            uneVignette["nomFichier"], True, COULEUR_TEXTE_DOUX
        )
        rectangleTexte = rendu.get_rect(
            midtop=(rectangleVignette.centerx, rectangleVignette.bottom + 6)
        )
        surfaceCible.blit(rendu, rectangleTexte)

    afficherTexteCentre(
        surfaceCible,
        "ESC pour quitter",
        polices["banniere"],
        COULEUR_TEXTE_DOUX,
        HAUTEUR_ECRAN - 24,
    )


def dessinerEcranResultat(
    surfaceCible, fondPrerendu, polices, banniere, vignetteSelection, predictions, rectangleRetour
):
    surfaceCible.blit(fondPrerendu, (0, 0))
    dessinerBanniere(surfaceCible, polices, banniere)

    afficherTexteCentre(
        surfaceCible,
        "Identification de l'animal",
        polices["titre"],
        COULEUR_TEXTE_PRINCIPAL,
        80,
    )

    # Photo agrandie a gauche.
    surfaceAgrandie = vignetteSelection["surfaceAgrandie"]
    largeurAgrandie, hauteurAgrandie = surfaceAgrandie.get_size()
    positionXImage = 80
    positionYImage = 140
    rectangleImage = pygame.Rect(positionXImage, positionYImage, largeurAgrandie, hauteurAgrandie)

    # Cadre derriere l'image.
    rectangleCadreImage = rectangleImage.inflate(20, 20)
    pygame.draw.rect(surfaceCible, COULEUR_CARTE, rectangleCadreImage, border_radius=12)
    pygame.draw.rect(
        surfaceCible, COULEUR_VIGNETTE_BORDURE,
        rectangleCadreImage, width=2, border_radius=12,
    )
    surfaceCible.blit(surfaceAgrandie, rectangleImage.topleft)

    afficherTexteEncadre(
        surfaceCible,
        vignetteSelection["nomFichier"],
        polices["info"],
        COULEUR_TEXTE_DOUX,
        rectangleCadreImage.left,
        rectangleCadreImage.bottom + 10,
    )

    # Bloc resultats a droite.
    positionXResultats = rectangleCadreImage.right + 60
    positionYResultats = 150
    largeurBloc = LARGEUR_ECRAN - positionXResultats - 60

    afficherTexteEncadre(
        surfaceCible,
        "Top 3 predictions du modele",
        polices["resultatTitre"],
        COULEUR_TEXTE_PRINCIPAL,
        positionXResultats,
        positionYResultats,
    )

    positionYLigne = positionYResultats + 60
    hauteurLigne = 90

    for rangCourant, (libelle, probabilite) in enumerate(predictions):
        # Numero de rang en gros.
        afficherTexteEncadre(
            surfaceCible,
            f"{rangCourant + 1}.",
            polices["resultatProba"],
            COULEUR_ACCENT,
            positionXResultats,
            positionYLigne,
        )

        # Libelle predit.
        afficherTexteEncadre(
            surfaceCible,
            libelle,
            polices["resultatLigne"],
            COULEUR_TEXTE_PRINCIPAL,
            positionXResultats + 36,
            positionYLigne,
        )

        # Pourcentage en bout de ligne.
        textePourcentage = f"{probabilite * 100:5.1f}%"
        renduProba = polices["resultatProba"].render(
            textePourcentage, True, COULEUR_TEXTE_PRINCIPAL
        )
        positionXProba = positionXResultats + largeurBloc - renduProba.get_width()
        surfaceCible.blit(renduProba, (positionXProba, positionYLigne))

        # Barre de progression sous la ligne.
        positionYBarre = positionYLigne + 38
        hauteurBarre = 18
        rectangleFondBarre = pygame.Rect(
            positionXResultats + 36,
            positionYBarre,
            largeurBloc - 36,
            hauteurBarre,
        )
        pygame.draw.rect(surfaceCible, COULEUR_BARRE_FOND, rectangleFondBarre, border_radius=8)

        proportion = max(0.0, min(1.0, probabilite))
        largeurPleine = max(2, int(rectangleFondBarre.width * proportion))
        rectanglePlein = pygame.Rect(
            rectangleFondBarre.left,
            rectangleFondBarre.top,
            largeurPleine,
            rectangleFondBarre.height,
        )
        pygame.draw.rect(surfaceCible, COULEUR_BARRE_PLEINE, rectanglePlein, border_radius=8)

        positionYLigne += hauteurLigne

    # Avertissement si les pourcentages sont anemiques (signe de photo factice).
    probabiliteSommet = predictions[0][1] if predictions else 0
    if probabiliteSommet < 0.10:
        afficherTexteEncadre(
            surfaceCible,
            "Note : faible certitude, image probablement non realiste.",
            polices["info"],
            COULEUR_TEXTE_DOUX,
            positionXResultats,
            positionYLigne + 10,
        )

    # Action retour vers la galerie.
    pygame.draw.rect(surfaceCible, COULEUR_ACCENT, rectangleRetour, border_radius=14)
    afficherTexteCentre(
        surfaceCible,
        "Retour aux photos",
        polices["action"],
        COULEUR_TEXTE_INVERSE,
        rectangleRetour.centery,
    )


# -----------------------------------------------------------------------------
# Boucle principale
# -----------------------------------------------------------------------------

def boucleBorne():
    pygame.init()
    surfaceEcran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
    pygame.display.set_caption("Borne intelligente vision - zoo maritime")
    horloge = pygame.time.Clock()

    polices = chargerPolices()
    banniere = lireBanniereEnvironnement()
    fondPrerendu = fabriquerFondDegrade(COULEUR_FOND_HAUT, COULEUR_FOND_BAS)

    cheminsPhotos = listerPhotosDisponibles(REPERTOIRE_PHOTOS)
    if not cheminsPhotos:
        print(
            f"Aucune photo trouvee dans {REPERTOIRE_PHOTOS}. La borne ne peut rien afficher.",
            file=sys.stderr,
        )
        pygame.quit()
        sys.exit(1)

    largeurVignette = 280
    hauteurVignette = 180
    vignettes = chargerVignettes(cheminsPhotos, largeurVignette, hauteurVignette)
    rectanglesVignettes = calculerRectanglesVignettes(
        len(vignettes), largeurVignette, hauteurVignette
    )

    # Pre-chargement du modele : evite un gel a la premiere selection.
    afficherEcranChargement(surfaceEcran, fondPrerendu, polices, banniere)
    pygame.display.flip()
    initialiserClassifieur()

    largeurAction = 280
    hauteurAction = 56
    rectangleRetour = pygame.Rect(
        (LARGEUR_ECRAN - largeurAction) // 2,
        HAUTEUR_ECRAN - 80,
        largeurAction,
        hauteurAction,
    )

    etatCourant = "galerie"
    vignetteSelection = None
    predictions = []

    while True:
        horloge.tick(60)

        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                pygame.quit()
                return
            if evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
            if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
                if etatCourant == "galerie":
                    for indexVignette, unRectangle in enumerate(rectanglesVignettes):
                        rectangleCadre = unRectangle.inflate(16, 38)
                        rectangleCadre.move_ip(0, 8)
                        if rectangleCadre.collidepoint(evenement.pos):
                            vignetteSelection = vignettes[indexVignette]
                            predictions = lancerClassification(
                                surfaceEcran, fondPrerendu, polices, banniere,
                                vignetteSelection,
                            )
                            etatCourant = "resultat"
                            break
                elif etatCourant == "resultat":
                    if rectangleRetour.collidepoint(evenement.pos):
                        etatCourant = "galerie"
                        vignetteSelection = None
                        predictions = []

        positionSouris = pygame.mouse.get_pos()

        if etatCourant == "galerie":
            dessinerEcranGalerie(
                surfaceEcran, fondPrerendu, polices, banniere,
                vignettes, rectanglesVignettes, positionSouris,
            )
        elif etatCourant == "resultat":
            dessinerEcranResultat(
                surfaceEcran, fondPrerendu, polices, banniere,
                vignetteSelection, predictions, rectangleRetour,
            )

        pygame.display.flip()


def afficherEcranChargement(surfaceCible, fondPrerendu, polices, banniere):
    """Affiche un ecran d'attente pendant l'initialisation du modele ONNX."""
    surfaceCible.blit(fondPrerendu, (0, 0))
    dessinerBanniere(surfaceCible, polices, banniere)
    afficherTexteCentre(
        surfaceCible, "Chargement du modele de vision...",
        polices["titre"], COULEUR_TEXTE_PRINCIPAL, HAUTEUR_ECRAN // 2 - 20,
    )
    afficherTexteCentre(
        surfaceCible, "MobileNetV2 (ONNX runtime)",
        polices["sousTitre"], COULEUR_TEXTE_DOUX, HAUTEUR_ECRAN // 2 + 30,
    )


def lancerClassification(surfaceEcran, fondPrerendu, polices, banniere, vignetteSelection):
    """Affiche un mini-ecran d'attente puis lance l'inference. Retourne les top-3 predictions."""
    surfaceEcran.blit(fondPrerendu, (0, 0))
    dessinerBanniere(surfaceEcran, polices, banniere)
    afficherTexteCentre(
        surfaceEcran, "Analyse de l'image en cours...",
        polices["titre"], COULEUR_TEXTE_PRINCIPAL, HAUTEUR_ECRAN // 2,
    )
    pygame.display.flip()
    try:
        return classifierImage(vignetteSelection["chemin"], nombreResultats=3)
    except Exception as erreur:
        print(f"Echec de la classification : {erreur}", file=sys.stderr)
        return [("erreur de classification", 0.0)]


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
