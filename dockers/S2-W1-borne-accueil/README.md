# SI SUR UN SERVER C'EST http://192.46.222.166:8090

localhost:8090 sinon







# Labo - Demande 1 - Borne d'accueil du zoo

## Ce que le prestataire a livre

Le **studio creatif local** a developpe la borne d'accueil du Zoo maritime du Bas-Saint-Laurent : une application Next.js 14 (React) qui presente le plan du parc et les horaires de la journee. La borne sera installee dans le hall d'entree, sur un grand ecran tactile.

Le contenu se trouve dans le dossier `application/` :

```
application/
- package.json                          # next, react, react-dom
- next.config.mjs                       # config Next.js minimale
- app/
    - layout.js                         # squelette HTML racine
    - page.js                           # composant principal : carte + horaires
    - globals.css                       # styles de la borne (palette zoo)
```

L'application affiche :

- Une carte SVG interactive du parc avec les quatre pavillons (foret, marin, prairie, voyageurs). Touchez un pavillon, sa fiche descriptive apparait.
- Une vue alternative "Horaires" avec la liste des activites du jour et le marqueur visuel de la prochaine activite (heure courante mise a jour toutes les 30 secondes).
- Une bascule "Carte / Horaires" en haut a droite.

Aucune base de donnees, aucun backend : tout est cote client. Le rendu Next.js est statique, parfait pour une borne en mode kiosque.

## Tester le contenu sans Docker

Si Node.js >= 18 est installe sur votre poste, vous pouvez tester l'application en local :

```
cd application/
npm install
npm run dev
```

Puis ouvrez `http://localhost:3000/`. La carte du parc s'affiche, les pavillons reagissent au clic, la bascule fonctionne.

Si Node n'est pas installe, **vous testerez votre travail directement avec Docker** une fois le Dockerfile pret. C'est precisement l'interet du labo : fournir une image autonome qu'on peut executer n'importe ou sans rien installer.

## Votre travail

Voir l'enonce du **Livrable 2, Demande 1**. Vous devez emballer cette application Next.js dans une image Docker prete a deployer sur la borne du hall d'accueil.

Vous produirez (a cote du dossier `application/`) :

- Un `Dockerfile` (le multi-stage est presente plus bas comme amelioration facultative)
- Un `.dockerignore`
- Trois scripts de pilotage : `construire.sh`, `demarrer.sh`, `arreter.sh`
- Un `README.md` qui presente votre travail

L'image finale doit servir l'application sur un port HTTP (8090 conseille pour eviter les conflits avec d'autres services). Le visiteur ouvre `http://localhost:8090/` et voit la borne d'accueil.

### Approche minimale - Dockerfile en une seule etape

Le plus simple, et tout a fait acceptable pour ce labo d'initiation : un Dockerfile qui part de `node:20`, copie les sources, lance `npm install`, lance `npm run build` puis demarre `npm start`. L'image est plus grosse parce qu'elle embarque Node + npm + les sources + les `node_modules` complets, mais elle est tres lisible et chaque etudiant comprend chaque ligne. C'est l'approche recommandee pour une premiere fois.

### Pour aller plus loin - Dockerfile multi-stage (facultatif)

Si vous voulez reduire la taille de l'image finale, vous pouvez ecrire un Dockerfile en **deux etapes** :

1. Etape `node:20-slim` : installe les dependances, lance le build, produit le rendu statique ou le serveur Next prod.
2. Etape finale : copie uniquement le resultat (et les dependances de production minimales) dans une image plus legere.

Vous pouvez choisir de servir avec `next start` (Node + Next runtime) **ou** d'exporter en statique via `next build` + `next export` et de servir avec `nginx:alpine`. Les deux approches sont valides ; documentez votre choix dans le README.

Ce raffinement n'est **pas requis** pour la note de base. Il est mentionne ici parce que c'est le pattern qu'on retrouve en industrie et que vous le croiserez plus tard.

### Banniere d'identification

Comme pour les autres bornes du zoo, votre image doit porter une banniere visible dans l'interface : nom de l'etudiant, matricule, date de build. Trois variables disponibles dans le Dockerfile :

- `ARG NOM_ETUDIANT`
- `ARG MATRICULE`
- `ARG BUILD_DATE`

Pour les passer cote frontend, Next.js dispose du mecanisme `NEXT_PUBLIC_*` (variables d'environnement injectees dans le bundle au build). Documentez la chaine ARG -> ENV -> NEXT_PUBLIC dans votre README.

Bonus visible dans la grille d'evaluation : ajouter un quatrieme onglet (par exemple "Equipe du jour") qui demontre que vous avez compris la structure du composant React et que vous savez modifier le contenu sans casser le build.
