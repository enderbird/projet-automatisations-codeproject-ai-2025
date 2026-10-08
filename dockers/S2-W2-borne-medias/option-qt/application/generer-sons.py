"""
Generateur de sons pedagogiques pour la borne medias - encyclopedie sonore.

Synthese procedurale de tons et patterns simples qui evoquent les especes
du Zoo maritime du Bas-Saint-Laurent. Ces sons ne sont pas des enregistrements
reels : ce sont des representations educatives generees au build de l'image
Docker pour eviter d'embarquer des fichiers audio dans le depot git.

Usage : python generer-sons.py <repertoire-cible>
"""

import math
import os
import struct
import sys
import wave

TAUX_ECHANTILLONNAGE = 22050


def fabriquerSilence(dureeSeconde):
    """Liste de samples a zero pour separer deux phrases sonores."""
    return [0] * int(TAUX_ECHANTILLONNAGE * dureeSeconde)


def fabriquerTon(frequenceHertz, dureeSeconde, amplitude=0.45, vibrato=0.0):
    """
    Onde sinusoidale simple avec enveloppe d'attaque-relachement et vibrato optionnel.
    Retourne une liste de samples 16-bit.
    """
    nombreEchantillons = int(TAUX_ECHANTILLONNAGE * dureeSeconde)
    samples = []
    duree_attaque = 0.04 * TAUX_ECHANTILLONNAGE
    for indexEchantillon in range(nombreEchantillons):
        tempsSeconde = indexEchantillon / TAUX_ECHANTILLONNAGE
        enveloppeAttaque = min(1.0, indexEchantillon / max(1.0, duree_attaque))
        enveloppeRelachement = max(0.0, 1.0 - (indexEchantillon / nombreEchantillons))
        enveloppe = enveloppeAttaque * enveloppeRelachement
        modulation = 1.0 + vibrato * math.sin(2 * math.pi * 6 * tempsSeconde)
        valeur = (
            math.sin(2 * math.pi * frequenceHertz * modulation * tempsSeconde)
            * amplitude
            * enveloppe
        )
        samples.append(int(valeur * 32767))
    return samples


def fabriquerGlissando(frequenceDepart, frequenceArrivee, dureeSeconde, amplitude=0.4):
    """Onde sinusoidale dont la frequence glisse lineairement de depart a arrivee."""
    nombreEchantillons = int(TAUX_ECHANTILLONNAGE * dureeSeconde)
    samples = []
    phaseAccumulee = 0.0
    for indexEchantillon in range(nombreEchantillons):
        progression = indexEchantillon / nombreEchantillons
        frequenceCourante = frequenceDepart + (frequenceArrivee - frequenceDepart) * progression
        phaseAccumulee += 2 * math.pi * frequenceCourante / TAUX_ECHANTILLONNAGE
        enveloppe = min(1.0, indexEchantillon / (0.05 * TAUX_ECHANTILLONNAGE)) * max(
            0.0, 1.0 - progression
        )
        valeur = math.sin(phaseAccumulee) * amplitude * enveloppe
        samples.append(int(valeur * 32767))
    return samples


def fabriquerBourdonnement(frequenceHertz, dureeSeconde, amplitude=0.35):
    """Bourdonnement type insecte : sinusoide modulee en amplitude rapide."""
    nombreEchantillons = int(TAUX_ECHANTILLONNAGE * dureeSeconde)
    samples = []
    for indexEchantillon in range(nombreEchantillons):
        tempsSeconde = indexEchantillon / TAUX_ECHANTILLONNAGE
        modulationAmplitude = 0.5 + 0.5 * math.sin(2 * math.pi * 80 * tempsSeconde)
        enveloppe = min(1.0, indexEchantillon / (0.03 * TAUX_ECHANTILLONNAGE)) * max(
            0.0, 1.0 - (indexEchantillon / nombreEchantillons)
        )
        valeur = (
            math.sin(2 * math.pi * frequenceHertz * tempsSeconde)
            * modulationAmplitude
            * amplitude
            * enveloppe
        )
        samples.append(int(valeur * 32767))
    return samples


def concatener(*listesSamples):
    """Met bout a bout plusieurs listes de samples."""
    resultat = []
    for uneListe in listesSamples:
        resultat.extend(uneListe)
    return resultat


def normaliser(samples):
    """Borne les valeurs entre -32767 et 32767 pour eviter le clipping."""
    return [max(-32767, min(32767, unSample)) for unSample in samples]


def ecrireFichierWav(cheminFichier, samples):
    """Ecrit une liste de samples en mono 16-bit dans un fichier .wav."""
    with wave.open(cheminFichier, "wb") as fichierWav:
        fichierWav.setnchannels(1)
        fichierWav.setsampwidth(2)
        fichierWav.setframerate(TAUX_ECHANTILLONNAGE)
        donneesPackees = struct.pack(
            "<%dh" % len(samples), *normaliser(samples)
        )
        fichierWav.writeframes(donneesPackees)


def fabriquerSonBeluga():
    """Beluga : chant aigu modulant entre 800 et 1800 Hz, on l'appelle 'le canari des mers'."""
    return concatener(
        fabriquerGlissando(900, 1700, 0.4),
        fabriquerSilence(0.1),
        fabriquerGlissando(1500, 800, 0.5),
        fabriquerSilence(0.15),
        fabriquerGlissando(700, 1400, 0.6),
    )


def fabriquerSonPhoque():
    """Phoque : aboyement bref et bas vers 220 Hz."""
    return concatener(
        fabriquerTon(220, 0.25, vibrato=0.02),
        fabriquerSilence(0.15),
        fabriquerTon(180, 0.3, vibrato=0.02),
        fabriquerSilence(0.2),
        fabriquerTon(220, 0.25, vibrato=0.02),
    )


def fabriquerSonOrignal():
    """Orignal : meuglement long et grave 130 Hz avec vibrato."""
    return fabriquerTon(130, 1.6, amplitude=0.5, vibrato=0.04)


def fabriquerSonGoeland():
    """Goeland : cris aigus repetes vers 1500 Hz."""
    return concatener(
        fabriquerTon(1500, 0.18),
        fabriquerSilence(0.08),
        fabriquerTon(1700, 0.18),
        fabriquerSilence(0.08),
        fabriquerTon(1400, 0.22),
        fabriquerSilence(0.12),
        fabriquerTon(1600, 0.2),
    )


def fabriquerSonBernache():
    """Bernache : trompette alternee a 600 Hz puis 700 Hz."""
    return concatener(
        fabriquerTon(600, 0.4, vibrato=0.01),
        fabriquerSilence(0.1),
        fabriquerTon(720, 0.5, vibrato=0.015),
    )


def fabriquerSonHuart():
    """Plongeon huard : cri long modulant entre 600 et 900 Hz."""
    return concatener(
        fabriquerGlissando(600, 900, 0.7, amplitude=0.45),
        fabriquerSilence(0.2),
        fabriquerGlissando(900, 700, 0.8, amplitude=0.45),
    )


def fabriquerSonAbeille():
    """Abeille : bourdonnement continu vers 250 Hz avec modulation 80 Hz."""
    return fabriquerBourdonnement(250, 1.5)


def fabriquerSonSterneArctique():
    """Sterne arctique : staccato aigu vers 2200 Hz."""
    elements = []
    for _index in range(7):
        elements.append(fabriquerTon(2200, 0.08, amplitude=0.4))
        elements.append(fabriquerSilence(0.08))
    return concatener(*elements)


def fabriquerSonHomard():
    """Homard : claquement de pince - bruits brefs et secs simules par burst basse frequence."""
    elements = []
    for _index in range(4):
        elements.append(fabriquerTon(80, 0.04, amplitude=0.6))
        elements.append(fabriquerSilence(0.3))
    return concatener(*elements)


CATALOGUE_SONS = {
    "beluga.wav": fabriquerSonBeluga,
    "phoque.wav": fabriquerSonPhoque,
    "orignal.wav": fabriquerSonOrignal,
    "goeland.wav": fabriquerSonGoeland,
    "bernache.wav": fabriquerSonBernache,
    "huart.wav": fabriquerSonHuart,
    "abeille.wav": fabriquerSonAbeille,
    "sterne-arctique.wav": fabriquerSonSterneArctique,
    "homard.wav": fabriquerSonHomard,
}


def main():
    if len(sys.argv) < 2:
        print("Usage : python generer-sons.py <repertoire-cible>", file=sys.stderr)
        sys.exit(1)
    repertoireSortie = sys.argv[1]
    os.makedirs(repertoireSortie, exist_ok=True)
    for nomFichier, fabricant in CATALOGUE_SONS.items():
        cheminComplet = os.path.join(repertoireSortie, nomFichier)
        ecrireFichierWav(cheminComplet, fabricant())
        print(f"  - {nomFichier} ({os.path.getsize(cheminComplet)} octets)")
    print(f"{len(CATALOGUE_SONS)} sons generes dans {repertoireSortie}")


if __name__ == "__main__":
    main()
