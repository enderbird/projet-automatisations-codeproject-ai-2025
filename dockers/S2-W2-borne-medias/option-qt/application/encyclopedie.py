"""
Borne medias - Encyclopedie sonore Qt (PySide6)
Zoo maritime du Bas-Saint-Laurent

Application kiosque qui presente une liste d'especes du Saint-Laurent.
Au clic sur une espece, sa fiche s'affiche avec un bouton qui declenche
le son pedagogique associe (genere proceduralement au build de l'image).
"""

import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt, QUrl, Slot
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

REPERTOIRE_SONS = Path(__file__).resolve().parent / "sons"

COULEURS_PAVILLON = {
    "marin": "#3d96bd",
    "foret": "#82a04c",
    "prairie": "#bd953a",
    "voyageurs": "#97633a",
}

NOMS_PAVILLON = {
    "marin": "Pavillon marin",
    "foret": "Pavillon foret",
    "prairie": "Pavillon prairie",
    "voyageurs": "Pavillon voyageurs",
}

ESPECES = [
    {
        "cle": "beluga",
        "nom": "Beluga",
        "nomLatin": "Delphinapterus leucas",
        "pavillon": "marin",
        "fichierSon": "beluga.wav",
        "description": (
            "Petite baleine blanche endemique du Saint-Laurent. Le beluga vit en "
            "troupeaux et communique par un repertoire vocal exceptionnellement "
            "riche, ce qui lui vaut le surnom de canari des mers. La population "
            "de l'estuaire est evaluee a moins de mille individus."
        ),
    },
    {
        "cle": "phoque",
        "nom": "Phoque commun",
        "nomLatin": "Phoca vitulina",
        "pavillon": "marin",
        "fichierSon": "phoque.wav",
        "description": (
            "Pinnipede observable sur les rochers de Tadoussac et de la Gaspesie. "
            "Le phoque commun plonge en moyenne entre 5 et 15 minutes pour pecher "
            "harengs, capelans et eperlans. Sa robe varie du gris au brun tachete."
        ),
    },
    {
        "cle": "homard",
        "nom": "Homard",
        "nomLatin": "Homarus americanus",
        "pavillon": "marin",
        "fichierSon": "homard.wav",
        "description": (
            "Crustace decapode des fonds rocheux du golfe. Le homard americain "
            "claque ses pinces pour signaler sa presence et chasse a la nuit. "
            "Sa carapace devient rouge a la cuisson : vivant, il est brun-vert."
        ),
    },
    {
        "cle": "orignal",
        "nom": "Orignal",
        "nomLatin": "Alces alces",
        "pavillon": "foret",
        "fichierSon": "orignal.wav",
        "description": (
            "Plus grand cervide d'Amerique du Nord. L'orignal male peut peser "
            "plus de 600 kg et porte un panache pouvant atteindre 1.6 m "
            "d'envergure. Le brame du male resonne en foret durant la rut "
            "automnale."
        ),
    },
    {
        "cle": "huart",
        "nom": "Plongeon huard",
        "nomLatin": "Gavia immer",
        "pavillon": "voyageurs",
        "fichierSon": "huart.wav",
        "description": (
            "Oiseau pecheur des lacs du bouclier canadien. Le huart est connu "
            "pour son chant module et porteur, qui s'entend sur plusieurs "
            "kilometres au crepuscule. Il figure sur la piece de un dollar "
            "canadien."
        ),
    },
    {
        "cle": "goeland",
        "nom": "Goeland argente",
        "nomLatin": "Larus argentatus",
        "pavillon": "voyageurs",
        "fichierSon": "goeland.wav",
        "description": (
            "Oiseau marin commun le long du Saint-Laurent. Le goeland est un "
            "opportuniste : il peche, charogne, et frequente les ports. Son "
            "cri rauque caracterise l'ambiance sonore des berges du fleuve."
        ),
    },
    {
        "cle": "bernache",
        "nom": "Bernache du Canada",
        "nomLatin": "Branta canadensis",
        "pavillon": "voyageurs",
        "fichierSon": "bernache.wav",
        "description": (
            "Grande oie migratrice qui survole le Quebec en formation V au "
            "printemps et en automne. La formation V economise jusqu'a 70% "
            "de l'energie de vol grace aux courants ascendants generes par "
            "l'oiseau de tete."
        ),
    },
    {
        "cle": "sterne-arctique",
        "nom": "Sterne arctique",
        "nomLatin": "Sterna paradisaea",
        "pavillon": "voyageurs",
        "fichierSon": "sterne-arctique.wav",
        "description": (
            "Detentrice du record de la plus longue migration animale connue : "
            "plus de 70 000 km annuels entre l'Arctique et l'Antarctique. "
            "Une sterne voit deux etes par an et peut vivre plus de 30 ans, "
            "soit l'equivalent de trois aller-retour vers la Lune."
        ),
    },
    {
        "cle": "abeille",
        "nom": "Abeille domestique",
        "nomLatin": "Apis mellifera",
        "pavillon": "prairie",
        "fichierSon": "abeille.wav",
        "description": (
            "Pollinisateur indispensable des cultures du Bas-Saint-Laurent. "
            "L'abeille porte deux paires d'ailes (quatre ailes au total) et "
            "communique la position des fleurs a ses soeurs par une danse "
            "frenetique au retour a la ruche."
        ),
    },
]


def lireBanniereEnvironnement():
    """Lit les variables d'environnement injectees au build (ARG du Dockerfile)."""
    return {
        "buildDate": os.environ.get("BUILD_DATE", "inconnu"),
        "nomEtudiant": os.environ.get("NOM_ETUDIANT", "anonyme"),
        "matricule": os.environ.get("MATRICULE", "000000"),
    }


class FenetreEncyclopedie(QMainWindow):
    """Fenetre principale de la borne medias : liste a gauche, fiche a droite."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Borne medias - Encyclopedie sonore du Zoo maritime")
        self.resize(1280, 720)

        self.banniere = lireBanniereEnvironnement()
        self.especeCourante = None

        self._lecteurAudio = QMediaPlayer(self)
        self._sortieAudio = QAudioOutput(self)
        self._lecteurAudio.setAudioOutput(self._sortieAudio)

        self._construireInterface()
        self._chargerListeEspeces()
        self._installerRaccourcis()

    def _construireInterface(self):
        widgetCentral = QWidget()
        self.setCentralWidget(widgetCentral)
        boiteVerticalePrincipale = QVBoxLayout(widgetCentral)
        boiteVerticalePrincipale.setContentsMargins(0, 0, 0, 0)
        boiteVerticalePrincipale.setSpacing(0)

        boiteVerticalePrincipale.addWidget(self._fabriquerBanniere())

        boiteHorizontaleContenu = QHBoxLayout()
        boiteHorizontaleContenu.setContentsMargins(20, 20, 20, 20)
        boiteHorizontaleContenu.setSpacing(20)

        self._listeEspeces = QListWidget()
        self._listeEspeces.setObjectName("liste-especes")
        self._listeEspeces.setFixedWidth(360)
        self._listeEspeces.setStyleSheet(
            """
            QListWidget {
                background: #fffdf6;
                border: 1px solid #d8d2bd;
                border-radius: 12px;
                padding: 6px;
                font-size: 18px;
            }
            QListWidget::item {
                padding: 14px 12px;
                border-radius: 8px;
            }
            QListWidget::item:selected {
                background: #1f4d2c;
                color: #ffffff;
            }
            """
        )
        self._listeEspeces.currentRowChanged.connect(self._afficherEspeceCouranteDepuisIndex)
        boiteHorizontaleContenu.addWidget(self._listeEspeces)

        boiteFiche = QWidget()
        boiteFiche.setObjectName("boite-fiche")
        boiteFiche.setStyleSheet(
            """
            #boite-fiche {
                background: #fffdf6;
                border: 1px solid #d8d2bd;
                border-radius: 12px;
            }
            """
        )
        boiteVerticaleFiche = QVBoxLayout(boiteFiche)
        boiteVerticaleFiche.setContentsMargins(28, 28, 28, 28)
        boiteVerticaleFiche.setSpacing(14)

        self._etiquettePavillon = QLabel("")
        self._etiquettePavillon.setObjectName("fiche-pavillon")
        policePavillon = QFont()
        policePavillon.setPointSize(11)
        policePavillon.setBold(True)
        self._etiquettePavillon.setFont(policePavillon)
        boiteVerticaleFiche.addWidget(self._etiquettePavillon)

        self._etiquetteNom = QLabel("")
        self._etiquetteNom.setObjectName("fiche-nom")
        policeNom = QFont()
        policeNom.setPointSize(28)
        policeNom.setBold(True)
        self._etiquetteNom.setFont(policeNom)
        boiteVerticaleFiche.addWidget(self._etiquetteNom)

        self._etiquetteNomLatin = QLabel("")
        self._etiquetteNomLatin.setObjectName("fiche-nom-latin")
        policeLatin = QFont()
        policeLatin.setPointSize(13)
        policeLatin.setItalic(True)
        self._etiquetteNomLatin.setFont(policeLatin)
        self._etiquetteNomLatin.setStyleSheet("color: #5a5a5a;")
        boiteVerticaleFiche.addWidget(self._etiquetteNomLatin)

        self._etiquetteDescription = QLabel("")
        self._etiquetteDescription.setObjectName("fiche-description")
        self._etiquetteDescription.setWordWrap(True)
        policeDescription = QFont()
        policeDescription.setPointSize(13)
        self._etiquetteDescription.setFont(policeDescription)
        self._etiquetteDescription.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        boiteVerticaleFiche.addWidget(self._etiquetteDescription, stretch=1)

        self._actionEcouter = QPushButton("Ecouter le son")
        self._actionEcouter.setObjectName("action-ecouter")
        self._actionEcouter.setMinimumHeight(60)
        self._actionEcouter.setStyleSheet(
            """
            QPushButton {
                background: #d23030;
                color: #ffffff;
                border: none;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #b62828;
            }
            QPushButton:disabled {
                background: #c0b8a8;
            }
            """
        )
        self._actionEcouter.clicked.connect(self._declencherLectureSon)
        boiteVerticaleFiche.addWidget(self._actionEcouter)

        boiteHorizontaleContenu.addWidget(boiteFiche, stretch=1)
        boiteVerticalePrincipale.addLayout(boiteHorizontaleContenu, stretch=1)

    def _fabriquerBanniere(self):
        boiteBanniere = QWidget()
        boiteBanniere.setObjectName("banniere")
        boiteBanniere.setFixedHeight(48)
        boiteBanniere.setStyleSheet(
            """
            #banniere {
                background: #1f4d2c;
                color: #ffffff;
            }
            #banniere QLabel {
                color: #ffffff;
            }
            """
        )
        boiteHorizontale = QHBoxLayout(boiteBanniere)
        boiteHorizontale.setContentsMargins(20, 0, 20, 0)
        etiquetteGauche = QLabel(
            "Borne medias - Encyclopedie sonore du Zoo maritime du Bas-Saint-Laurent"
        )
        policeBanniere = QFont()
        policeBanniere.setPointSize(10)
        policeBanniere.setBold(True)
        etiquetteGauche.setFont(policeBanniere)
        boiteHorizontale.addWidget(etiquetteGauche)
        boiteHorizontale.addStretch()
        etiquetteDroite = QLabel(
            f"{self.banniere['nomEtudiant']} - {self.banniere['matricule']} "
            f"- build {self.banniere['buildDate']}"
        )
        etiquetteDroite.setFont(policeBanniere)
        boiteHorizontale.addWidget(etiquetteDroite)
        return boiteBanniere

    def _chargerListeEspeces(self):
        for uneEspece in ESPECES:
            elementListe = QListWidgetItem(uneEspece["nom"])
            elementListe.setData(Qt.UserRole, uneEspece["cle"])
            self._listeEspeces.addItem(elementListe)
        if self._listeEspeces.count() > 0:
            self._listeEspeces.setCurrentRow(0)

    def _installerRaccourcis(self):
        raccourciFermer = QShortcut(QKeySequence(Qt.Key_Escape), self)
        raccourciFermer.activated.connect(self.close)
        raccourciJouer = QShortcut(QKeySequence(Qt.Key_Space), self)
        raccourciJouer.activated.connect(self._declencherLectureSon)

    @Slot(int)
    def _afficherEspeceCouranteDepuisIndex(self, indexLigne):
        if indexLigne < 0 or indexLigne >= len(ESPECES):
            return
        especeChoisie = ESPECES[indexLigne]
        self.especeCourante = especeChoisie
        couleurPavillon = COULEURS_PAVILLON.get(especeChoisie["pavillon"], "#5a5a5a")
        self._etiquettePavillon.setText(NOMS_PAVILLON[especeChoisie["pavillon"]].upper())
        self._etiquettePavillon.setStyleSheet(
            f"color: {couleurPavillon}; letter-spacing: 0.08em;"
        )
        self._etiquetteNom.setText(especeChoisie["nom"])
        self._etiquetteNomLatin.setText(especeChoisie["nomLatin"])
        self._etiquetteDescription.setText(especeChoisie["description"])

    @Slot()
    def _declencherLectureSon(self):
        if self.especeCourante is None:
            return
        cheminSon = REPERTOIRE_SONS / self.especeCourante["fichierSon"]
        if not cheminSon.exists():
            self._etiquetteDescription.setText(
                f"Son introuvable : {cheminSon}\n\n"
                "Le fichier audio est genere au build de l'image Docker. "
                "Reconstruis l'image avec ./construire.sh."
            )
            return
        self._lecteurAudio.stop()
        self._lecteurAudio.setSource(QUrl.fromLocalFile(str(cheminSon)))
        self._sortieAudio.setVolume(0.85)
        self._lecteurAudio.play()


def main():
    application = QApplication(sys.argv)
    application.setApplicationName("Borne medias - Encyclopedie sonore")
    fenetre = FenetreEncyclopedie()
    fenetre.show()
    return application.exec()


if __name__ == "__main__":
    sys.exit(main())
