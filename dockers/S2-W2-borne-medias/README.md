# Labo - Demande 2 - Borne medias interactive

## Ce que le prestataire a livre

Trois bornes medias prototypes, chacune dans un toolkit different, ont ete livrees par le **studio creatif local**. Le visiteur, devant la borne, vit une experience interactive sur les especes du Saint-Laurent : quiz, encyclopedie sonore, ou jeu 3D selon la version installee.

**Vous choisissez une seule des trois options** au demarrage du labo. Le travail Docker a faire est equivalent dans les trois cas, seule la stack a emballer change.

```
demande-2-borne-medias/
- option-pygame/                # Quiz Pygame, app native SDL2
    - application/
        - quiz.py
- option-qt/                    # Encyclopedie sonore PySide6 (Qt6)
    - application/
        - encyclopedie.py
        - generer-sons.py
- option-threejs/               # Mini-jeu 3D WebGL (three.js + Vite)
    - index.html
    - package.json
    - vite.config.js
    - src/
        - main.js
        - decoration/
            - style.css
```

### Option Pygame - Quiz interactif (app non-web)

Application Python/Pygame qui pose dix questions a choix multiples sur la faune du Saint-Laurent. Fenetre 1280x720, mode kiosque, touchez l'ecran ou utilisez les touches 1-4. Score, explications, rejouable.

Stack : Python 3.12 + SDL2. Pas de serveur web, c'est une vraie app desktop affichee via X11.

### Option Qt - Encyclopedie sonore (app non-web)

Application PySide6 (Qt6 pour Python) qui presente neuf especes du zoo avec fiche detaillee et bouton "Ecouter le son". Les sons sont **synthetises proceduralement pendant le build de l'image Docker** (sinusoides, glissandos), pas embarques en binaire.

Stack : Python 3.12 + Qt6/XCB + GStreamer + PySide6. App desktop X11 + audio PulseAudio.

### Option three.js - Jeu 3D dans le navigateur (frontend web)

Mini-jeu 3D WebGL : sur le pont d'un bateau, le visiteur fait pivoter la camera et clique sur les belugas qui nagent autour. Compteur de score, message final.

Stack : three.js + Vite (build) + serveur web statique (Node ou nginx). Demonstration possible du **multi-stage Docker** en facultatif, mais une image en une seule etape qui sert le bundle suffit pour la note de base.

## Tester le contenu sans Docker

Selon l'option choisie :

- **Pygame** : `pip install pygame==2.5.2`, puis `cd option-pygame/application && python quiz.py`. Necessite un serveur X11 sur votre poste (Linux natif ou WSL2/XQuartz).
- **Qt** : `pip install PySide6==6.7.2`, puis `cd option-qt/application && python generer-sons.py sons/ && python encyclopedie.py`. Necessite Qt6 et PulseAudio.
- **three.js** : `cd option-threejs && npm install && npm run dev`, puis `http://localhost:5173/`. Aucune dependance graphique systeme.

Si vous n'avez pas l'environnement de test, vous **testerez avec Docker** une fois le Dockerfile pret.

## Votre travail

Voir l'enonce du **Livrable 2, Demande 2**. Vous devez emballer **une seule** des trois options dans une image Docker prete a deployer sur la borne medias du parc.

Vous produirez (a cote du dossier `application/` ou des sources de l'option choisie) :

- Un `Dockerfile`
- Un `.dockerignore` (ou `.gitignore` adapte)
- Trois scripts de pilotage : `construire.sh`, `demarrer.sh`, `arreter.sh`
- Un `README.md` qui presente votre travail

### Specificites par option

#### Option Pygame ou Qt (apps desktop X11)

- L'image n'expose **aucun port reseau** : ce n'est pas un serveur, c'est une app.
- Le container monte `/tmp/.X11-unix` et lit la variable `DISPLAY` pour afficher sa fenetre sur votre serveur X11.
- `demarrer.sh` doit appeler `xhost +local:docker` avant de demarrer (et `xhost -local:docker` dans `arreter.sh` pour ne pas laisser le serveur X expose).
- Pour Qt, `demarrer.sh` doit aussi monter le socket PulseAudio (`/run/user/$(id -u)/pulse/native`) pour que la lecture audio fonctionne.

#### Option three.js (frontend web)

- Le Dockerfile peut etre en **une seule etape** (approche d'initiation recommandee) : par exemple partir de `node:20`, lancer `npm install` puis `npm run build`, et servir le dossier `dist/` avec un serveur simple. Le multi-stage `node:20-slim` -> `nginx:1.27-alpine` est presente en option pour ceux qui veulent reduire la taille de l'image finale, mais ce n'est **pas obligatoire** pour ce labo d'initiation.
- `demarrer.sh` publie le port 80 (ou le port de votre serveur) du container sur 8091 de l'hote.

### Banniere d'identification

Comme pour toutes les bornes du zoo, votre image doit porter une banniere visible avec : nom etudiant, matricule, date de build. Trois variables ARG dans le Dockerfile :

- `ARG NOM_ETUDIANT`
- `ARG MATRICULE`
- `ARG BUILD_DATE`

Selon l'option :

- **Pygame / Qt** : `ARG` -> `ENV` -> lu au runtime par Python via `os.environ`, dessine en haut de la fenetre.
- **three.js** : `ARG` -> Vite remplace les identifiants `__NOM_ETUDIANT__` / `__MATRICULE__` / `__BUILD_DATE__` dans le bundle JavaScript via le mecanisme `define` (a configurer dans `vite.config.js`).

Documentez la chaine ARG -> banniere dans votre README, car c'est ce qui prouve que votre image et celle de votre voisin ne sont pas identiques.

### Pieges connus selon l'option

- **Pygame / Qt** : si la fenetre ne s'ouvre pas, c'est presque toujours un probleme X11. Verifiez que `echo $DISPLAY` n'est pas vide sur l'hote, et que vous avez bien fait `xhost +local:docker` avant le `docker run`.
- **Pygame** : ne lancez **pas** Pygame en `--restart unless-stopped` pendant le developpement. La moindre erreur Python relance en boucle et sature le terminal. Ajoutez ce drapeau seulement quand l'app est stable.
- **Qt** : les wheels PySide6 sont lourds (~150 Mo). Ne les ajoutez pas au `.dockerignore` si vous tentez d'optimiser. Le poids vient de Qt, c'est inevitable.
- **three.js** : le `.dockerignore` est **critique**. Si vous oubliez d'exclure `node_modules/`, votre `docker build` enverra plusieurs centaines de Mo au daemon a chaque rebuild. Le `.dockerignore` est aussi important que le Dockerfile.

Bonus visible dans la grille d'evaluation : pour Pygame, ajouter une question sur une espece de votre cegep d'attache (ex : oiseau du Bas-Saint-Laurent observable depuis votre fenetre). Pour Qt, ajouter une espece dans le catalogue avec son son synthetise. Pour three.js, ajouter un effet visuel (brouillard sur la mer, soleil couchant).
