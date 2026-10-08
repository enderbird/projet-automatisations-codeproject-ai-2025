# Labo - Demande 2 - Web flat

## Ce que le prestataire a livré

Le **studio créatif local** maintient une dizaine de mini-sites événementiels du zoo (festivals, journées thématiques, nuits des musées) avec un moteur de mini-CMS flat-file de leur cru.

Deux dossiers sont fournis :

### Le moteur (dossier `moteur/`)

Le moteur PHP du CMS, conçu pour tourner dans un environnement PHP + Apache.

```
moteur/
├── index.php                           # liste les articles
├── article.php                         # affiche un article
└── decoration/
    └── decoration-evenements.css       # style commun
```

### Le contenu (dossier `fp-content/`)

Trois articles d'exemple, stockés en HTML avec un bloc de métadonnées en commentaire.

```
fp-content/
└── articles/
    ├── festival-oiseaux-migrateurs-2026.html
    ├── journee-pollinisateurs-2026.html
    └── nuit-musees-marin-2026.html
```

## Le pattern important

**Le moteur et le contenu sont délibérément séparés**, parce qu'ils n'ont pas les mêmes droits d'écriture au zoo :

- `moteur/` est du **code**. Seul l'architecte logiciel y touche. Les fichiers PHP, le CSS du moteur, la logique d'affichage : c'est figé tant que personne n'y a touché côté technique.
- `fp-content/` est du **contenu**. Toute personne du zoo qui a une annonce à publier (chargé de communication, responsable des événements, bénévole délégué) y dépose un fichier HTML. Pas besoin de comprendre PHP, pas besoin de toucher au moteur.

Cette séparation des droits d'écriture est la raison d'être de l'architecture flat-file. Gardez-la en tête quand vous construirez votre Docker : la question "qui peut publier sans déranger le code ?" va revenir.

## Votre travail

Vous emballez ces fichiers dans une image Docker.

Le moteur PHP s'attend à trouver `fp-content/` au même niveau que `index.php` dans la hiérarchie servie. Votre `Dockerfile` doit donc `COPY` les deux dossiers à la bonne place : le contenu de `moteur/` dans le dossier servi par Apache, et `fp-content/` comme sous-dossier à côté de `index.php`. C'est exactement le `COPY` que vous venez d'apprendre.

Quand le studio publie un nouvel article, vous le déposez dans `fp-content/articles/`, vous relancez `construire.sh` puis `demarrer.sh`, et l'article apparait dans le navigateur.

Vous produirez (à côté des dossiers `moteur/` et `fp-content/`) :

- Un `Dockerfile`
- Un `.dockerignore`
- Trois scripts de pilotage : `construire.sh`, `demarrer.sh`, `arreter.sh`
- Un `README.md` qui présente votre travail

---

## Pour aller plus loin - le bonus (volumes Docker)

Avec la livraison ci-dessus, **chaque nouvel article publié par le studio oblige à reconstruire l'image**. Pour le studio créatif qui veut publier au fil de l'eau, ça reste pénible : l'image est figée et il faut votre intervention à chaque mise à jour.

Le bonus consiste à régler ce problème en montant le dossier `fp-content/` en **volume** au `docker run`, plutôt qu'en le copiant dans l'image. Le studio peut alors déposer un nouvel article dans `fp-content/articles/` et il apparait dans le conteneur **sans rebuild de l'image**.

Pour que ce bonus soit reconnu, vous déposez dans le dossier de la demande une **courte capture vidéo de preuve** (max 30 secondes) qui montre, dans l'ordre :

1. La liste des articles dans le navigateur avant l'ajout
2. La création d'un quatrième fichier dans `fp-content/articles/`
3. Le rafraichissement de la page qui fait apparaitre le nouvel article, sans avoir relancé `construire.sh`

La présence de la vidéo et la configuration du volume dans vos scripts suffisent : le correcteur verra que vous avez choisi cette voie.

### Tester ce comportement sans Docker (optionnel)

Si vous voulez voir le moteur tourner sans passer par Docker - utile pour explorer le code PHP avant ou après votre travail Docker - il faut contourner le fait que `fp-content/` n'est pas directement au bon niveau dans la livraison fournie. Créez un lien symbolique :

```
ln -s ../fp-content moteur/fp-content
php -S localhost:8000 -t moteur
```

Puis ouvrez `http://localhost:8000/`. Ce test local n'est pas demandé pour la note - il sert uniquement à votre exploration.
