## Comment lancer

### Prérequis

- Docker installé (`docker --version` pour vérifier)
- Être dans le dossier `S1-W1-page-html/`

### Séquence complète

```bash
# 1. Construire l'image
./construire.sh

# 2. Démarrer le container
./demarrer.sh

# 3. Ouvrir dans le navigateur
# http://localhost:8080/

# 4. Arrêter quand terminé
./arreter.sh
```

### Commandes utiles

```bash
# Voir le container en cours
docker ps

# Consulter les logs Apache
docker logs zoo-oiseaux-en-marche

# Vérifier le mappage de port
docker port zoo-oiseaux-en-marche
```

---
---
---
---
---
---
---
---




# Labo - Demande 1 - Pages HTML

## Ce que le prestataire a livré

Le **studio créatif local** et les **bénévoles artistes** ont produit, à l'âge doré du zoo, une encyclopédie HTML statique sur les oiseaux migrateurs du Saint-Laurent, accompagnée d'un mini-simulateur de vol en V-formation en p5.js.

Le contenu se trouve dans le dossier `contenu/` :

```
contenu/
├── index.html                          # accueil avec grille des 6 oiseaux
├── decoration/
│   └── decoration-encyclopedie.css     # style commun
├── oiseaux/
│   ├── bernache-du-canada.html
│   ├── oie-des-neiges.html
│   ├── plongeon-huard.html
│   ├── sterne-pierregarin.html
│   ├── becasseau-semipalme.html
│   └── goeland-argente.html
└── jeu-vol-oiseaux/
    └── index.html                      # simulation p5.js (CDN externe)
```

Aucune base de données, aucun backend. Que du HTML, du CSS et du JavaScript côté navigateur.

## Tester le contenu sans Docker

Vous pouvez ouvrir directement `contenu/index.html` dans un navigateur (clic droit -> Ouvrir avec). Le mini-jeu p5.js charge sa bibliothèque depuis un CDN, il faut donc une connexion Internet pour la première ouverture.

Pour un test plus proche d'un vrai serveur, vous pouvez aussi servir le dossier avec une commande comme `python3 -m http.server` depuis le dossier `contenu/` puis ouvrir `http://localhost:8000/`.

## Votre travail

Voir l'énoncé du **Livrable 1, Demande 1**. Vous devez emballer ce contenu dans une image Docker légère, prête à déployer sur la borne du pavillon des oiseaux migrateurs (Raspberry Pi sous Ubuntu Server ARM).

Vous produirez (à côté du dossier `contenu/`) :

- Un `Dockerfile`
- Un `.dockerignore`
- Trois scripts de pilotage : `construire.sh`, `demarrer.sh`, `arreter.sh`
- Un `README.md` qui présente votre travail

Aucun changement à apporter au contenu lui-même : il fonctionne déjà tel quel.
