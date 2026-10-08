"""
Classifieur d'images base sur MobileNetV2 ONNX.

Charge une seule fois le modele et les labels ImageNet, puis expose
classifierImage(cheminImage) qui retourne le top-3 sous forme
[(libelle, probabilite), ...].

Aucun acces reseau requis : modele et labels sont dans l'image Docker
(rapatries pendant le build, voir Dockerfile).
"""

import os

import numpy as np
import onnxruntime
from PIL import Image

CHEMIN_MODELE = "/borne/mobilenetv2-12.onnx"
CHEMIN_LABELS = "/borne/imagenet-labels.txt"

TAILLE_ENTREE = 224

# Constantes de normalisation ImageNet (mean / std par canal RGB).
MOYENNE_IMAGENET = np.array([0.485, 0.456, 0.406], dtype=np.float32)
ECART_TYPE_IMAGENET = np.array([0.229, 0.224, 0.225], dtype=np.float32)

# Singleton : on charge le modele une seule fois au premier appel.
_sessionInference = None
_listeLabels = None
_nomEntree = None


def chargerLabels(cheminFichier):
    """Lit synset.txt (1000 lignes 'wnid label1, label2') et retourne uniquement le premier libelle humain."""
    libellesHumains = []
    with open(cheminFichier, "r", encoding="utf-8") as fichier:
        for uneLigne in fichier:
            ligneNettoyee = uneLigne.strip()
            if not ligneNettoyee:
                continue
            # Format : "n01440764 tench, Tinca tinca". On garde "tench".
            partiesLigne = ligneNettoyee.split(" ", 1)
            if len(partiesLigne) == 2:
                libelleComplet = partiesLigne[1]
            else:
                libelleComplet = partiesLigne[0]
            libellePrincipal = libelleComplet.split(",")[0].strip()
            libellesHumains.append(libellePrincipal)
    return libellesHumains


def initialiserClassifieur():
    """Charge le modele ONNX et les labels une seule fois (singleton)."""
    global _sessionInference, _listeLabels, _nomEntree
    if _sessionInference is not None:
        return

    if not os.path.exists(CHEMIN_MODELE):
        raise FileNotFoundError(
            f"Modele ONNX absent : {CHEMIN_MODELE}. Le build n'a pas pu rapatrier mobilenetv2-12.onnx."
        )
    if not os.path.exists(CHEMIN_LABELS):
        raise FileNotFoundError(
            f"Fichier de labels absent : {CHEMIN_LABELS}."
        )

    optionsSession = onnxruntime.SessionOptions()
    optionsSession.intra_op_num_threads = 1
    optionsSession.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
    _sessionInference = onnxruntime.InferenceSession(
        CHEMIN_MODELE,
        sess_options=optionsSession,
        providers=["CPUExecutionProvider"],
    )
    _nomEntree = _sessionInference.get_inputs()[0].name
    _listeLabels = chargerLabels(CHEMIN_LABELS)


def preparerTenseurEntree(cheminImage):
    """Charge l'image, la passe en RGB 224x224 normalise ImageNet et retourne un tenseur NCHW float32."""
    imageSource = Image.open(cheminImage).convert("RGB")
    imageRedimensionnee = imageSource.resize((TAILLE_ENTREE, TAILLE_ENTREE), Image.BILINEAR)

    tableauPixels = np.asarray(imageRedimensionnee, dtype=np.float32) / 255.0
    tableauNormalise = (tableauPixels - MOYENNE_IMAGENET) / ECART_TYPE_IMAGENET

    # HWC -> CHW
    tableauTranspose = np.transpose(tableauNormalise, (2, 0, 1))
    # Ajout du batch -> NCHW
    tenseurEntree = np.expand_dims(tableauTranspose, axis=0).astype(np.float32)
    return tenseurEntree


def calculerSoftmax(vecteurLogits):
    """Softmax stable : on retire le max avant l'exp pour eviter les overflows."""
    vecteurDecale = vecteurLogits - np.max(vecteurLogits)
    exponentielles = np.exp(vecteurDecale)
    return exponentielles / np.sum(exponentielles)


def classifierImage(cheminImage, nombreResultats=3):
    """Classifie une image et retourne les top-N predictions (libelle, probabilite)."""
    initialiserClassifieur()

    tenseurEntree = preparerTenseurEntree(cheminImage)
    sortieReseau = _sessionInference.run(None, {_nomEntree: tenseurEntree})
    vecteurLogits = sortieReseau[0][0]
    vecteurProbabilites = calculerSoftmax(vecteurLogits)

    # argpartition est O(n), plus rapide que sort complet pour un top-K.
    indicesNonTries = np.argpartition(-vecteurProbabilites, nombreResultats)[:nombreResultats]
    indicesTriesParProbabilite = indicesNonTries[
        np.argsort(-vecteurProbabilites[indicesNonTries])
    ]

    resultats = []
    for indexClasse in indicesTriesParProbabilite:
        libelle = _listeLabels[indexClasse] if indexClasse < len(_listeLabels) else f"classe-{indexClasse}"
        probabilite = float(vecteurProbabilites[indexClasse])
        resultats.append((libelle, probabilite))
    return resultats


if __name__ == "__main__":
    # Petit test manuel : python classifieur.py /chemin/vers/image.jpg
    import sys
    if len(sys.argv) != 2:
        print("Usage : python classifieur.py <chemin-image>")
        sys.exit(1)
    cheminTest = sys.argv[1]
    predictions = classifierImage(cheminTest)
    for libelle, probabilite in predictions:
        print(f"{libelle:30s} {probabilite * 100:5.1f}%")
