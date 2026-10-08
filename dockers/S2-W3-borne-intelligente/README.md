# Labo - Demande 3 - Borne intelligente

## Ce que le prestataire a livre

Trois bornes intelligentes prototypes, chacune avec une approche IA differente, ont ete livrees par le **studio creatif local**. Le visiteur interagit avec une intelligence artificielle locale qui tourne **dans le container** : pas de cloud, pas d'API distante, pas de cle a payer, fonctionnement hors-ligne une fois l'image construite.

**Vous choisissez une seule des trois options** au demarrage du labo. Le travail Docker a faire est equivalent dans les trois cas, seule la facon dont l'IA est embarquee change.

```
demande-3-borne-intelligente/
- option-narrative/             # Aventure interactive avec LLM local (ollama)
    - application/
        - narrative.py
        - prompts.py
        - entrypoint.sh
- option-qa/                    # Q&A streame avec LLM local (ollama)
    - application/
        - qa.py
        - questions.py
        - entrypoint.sh
- option-vision/                # Classification d'images avec modele ONNX local
    - application/
        - vision.py
        - classifieur.py
        - generer-photos-test.py
```

### Option Narrative - Aventure LLM (ollama embarque)

Le visiteur incarne un soigneur stagiaire dans un des trois pavillons (marin, foret, prairie). L'IA pose le decor (3-4 phrases), propose 3 choix d'action (A/B/C), le visiteur clique son choix, l'IA poursuit l'histoire pendant 6 etapes, puis conclut.

Stack : Python/Pygame + serveur ollama (modele `qwen2.5:0.5b`, ~400 Mo). Tout dans le meme container, communication par localhost. Le modele est telecharge **au premier demarrage** dans un volume Docker persistant, pas pendant le build.

### Option Q&A - Reponses LLM streamees (ollama embarque)

Le visiteur choisit une question parmi 12 cartes pre-redigees (4 par ecosysteme). L'IA repond, et les jetons s'affichent au fur et a mesure (effet "ChatGPT en streaming") via l'API `stream: true` de ollama.

Stack : meme que narrative, **meme volume `zoo-ollama-cache` partage** : si vous lancez d'abord narrative puis qa (ou l'inverse), le modele n'est telecharge qu'une fois.

### Option Vision - Classification d'images (ONNX local)

Galerie 3x3 de photos d'animaux, clic sur une photo, le modele MobileNetV2 (charge via `onnxruntime`) renvoie les top-3 predictions affichees en barres horizontales. Aucun reseau au runtime.

Stack : Python/Pygame + onnxruntime (CPU) + Pillow + numpy. Le modele (`mobilenetv2-12.onnx`, ~14 Mo) et les labels sont **rapatries pendant le build** (URLs ONNX Model Zoo) et empaquetes dans l'image. Donc une fois construite, l'image est totalement autonome.

## Tester le contenu sans Docker

Selon l'option choisie :

- **Narrative ou Q&A** : il faut installer ollama localement (https://ollama.com/), faire `ollama pull qwen2.5:0.5b`, puis depuis `application/` faire `pip install pygame==2.5.2 requests==2.32.3 && python narrative.py` (ou `python qa.py`). Necessite X11.
- **Vision** : `pip install pygame==2.5.2 onnxruntime==1.18.1 Pillow==10.4.0 numpy==1.26.4`, telechargez `mobilenetv2-12.onnx` et `imagenet-labels.txt` (URLs documentees dans la solution), placez-les a cote de `vision.py`, generez les 9 photos factices avec `python generer-photos-test.py`, puis `python vision.py`. Necessite X11.

Honnetement : **vous testerez avec Docker** une fois le Dockerfile pret, c'est plus simple.

## Votre travail

Voir l'enonce du **Livrable 2, Demande 3**. Vous devez emballer **une seule** des trois options dans une image Docker prete a deployer sur la borne intelligente du parc.

Vous produirez (a cote du dossier `application/`) :

- Un `Dockerfile`
- Un script `entrypoint.sh` (deja fourni dans le materiel comme reference, vous pouvez l'adapter)
- Un `.gitignore`
- Trois scripts de pilotage : `construire.sh`, `demarrer.sh`, `arreter.sh`
- Un `README.md` qui presente votre travail

### Patterns Docker importants pour cette demande

Ce livrable illustre **trois patterns Docker** que vous devez savoir expliquer pendant la correction :

1. **Plusieurs processus dans un meme container** (options Narrative et Q&A : ollama serve + python xxx.py). Un script `entrypoint.sh` les orchestre : lance ollama en arriere-plan, attend qu'il reponde, pull le modele si necessaire, lance Python.
2. **Donnees lourdes au runtime via volume nomme** (options Narrative et Q&A) : le modele de 400 Mo n'est pas dans l'image (l'image resterait grosse et impossible a pousser dans un registre), il vit dans un volume Docker persistant `zoo-ollama-cache` cree par `demarrer.sh` la premiere fois.
3. **Donnees lourdes au build et image autonome** (option Vision) : le modele de 14 Mo est telecharge pendant le build (`RUN wget ...`) et empaquete. L'image est plus grosse mais elle fonctionne hors-ligne immediatement.

Le choix entre ces patterns depend du poids des donnees (le LLM est trop gros pour l'image, le modele de vision est juste assez petit) et de la frequence de mise a jour (le LLM peut changer, le modele de vision est fige).

### Specificites par option

#### Pour Narrative ou Q&A (ollama embarque)

- Installer ollama dans le Dockerfile via le script officiel : `RUN curl -fsSL https://ollama.com/install.sh | sh`.
- Le port `11434` reste **prive** dans le container (ollama ecoute sur 127.0.0.1, Python lui parle en localhost).
- Le volume nomme `zoo-ollama-cache` est cree par `demarrer.sh` (ou par votre `entrypoint.sh`) et monte sur `/root/.ollama`.
- Affichez un message clair la premiere fois : "Premier demarrage, telechargement du modele en cours, 2 a 3 minutes...". Sans ca, l'utilisateur croit que la borne plante.

#### Pour Vision (ONNX local)

- Telecharger les artefacts pendant le build avec `wget` : modele depuis le ONNX Model Zoo, labels depuis le meme repo. Documentez les URLs en commentaire dans le Dockerfile.
- **Aucun volume**, **aucun port reseau** : l'image est immuable et autonome.
- Le modele est charge **une seule fois** au demarrage de Python (singleton), pas a chaque clic. Verifiez avec `top` que le premier clic ne reload rien.
- Les 9 photos factices generees pendant le build donnent des predictions absurdes (`envelope`, `menu`, `carton`). C'est attendu et c'est la lecon : le pipeline marche, le contenu d'entree est ce qui compte. Vous pouvez le mentionner dans votre README pour montrer que vous avez compris.

### Banniere d'identification

Meme convention que les autres bornes : `ARG NOM_ETUDIANT`, `ARG MATRICULE`, `ARG BUILD_DATE` injectees au build, `ENV` qui les persiste, lecture par Python via `os.environ`, affichage en haut de chaque ecran.

Bonus visible dans la grille d'evaluation : reduire le temps de premier demarrage (Narrative/Q&A) ou la taille de l'image (Vision) par rapport au baseline. Mesurez et documentez vos chiffres dans le README.
