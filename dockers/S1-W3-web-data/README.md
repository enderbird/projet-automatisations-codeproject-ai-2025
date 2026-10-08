# TESTER AVEC 

sudo docker run -p 8080:80 zoo-catalogue-especes:latest


---
---
---
---
---
---
---




# Labo - Demande 3 - Web et données

## Ce que le prestataire a livré

Une **stagiaire en informatique** a écrit une petite application PHP qui interroge une base **MariaDB** pour afficher le catalogue des espèces du zoo. Le visiteur scrolle, filtre par écosystème, voit la fiche détaillée d'une espèce.

Deux livrables :

### L'application PHP (dossier `application/`)

```
application/
├── connexion-bd.php                    # fonction d'ouverture PDO + helper écosystème
├── index.php                           # liste filtrable
├── fiche.php                           # détail d'une espèce
└── decoration/
    └── decoration-catalogue.css        # style commun
```

L'application utilise PDO MySQL (extension PHP standard) et s'attend à trouver une base `catalogue_especes` accessible sur `localhost`, sans mot de passe pour l'utilisateur `root` (configuration locale du container, pas exposée à l'extérieur).

### Le schéma SQL (fichier `schema.sql`)

Le schéma initial avec la table `espece` et **12 espèces de démonstration** réparties sur les 4 écosystèmes du zoo (3 par écosystème). Le schéma est conçu pour être joué une seule fois au tout premier démarrage.

## Tester sans Docker

L'application nécessite à la fois PHP et MariaDB installés sur votre poste, plus la création de la base et le chargement du schéma. C'est exactement la complexité que Docker va simplifier. Pour ce labo, **vous testerez votre travail directement avec Docker** une fois votre Dockerfile et votre script de démarrage prêts.

Si vous tenez à inspecter le code en avance, vous pouvez ouvrir les fichiers PHP dans un éditeur : ils sont courts et lisibles, vous comprendrez rapidement comment ils fonctionnent.

## Votre travail

Voir l'énoncé du **Livrable 1, Demande 3**. Vous devez emballer **PHP, Apache et MariaDB dans une seule image Docker**, avec un script de démarrage maison qui orchestre les deux processus. Pas de docker-compose cette année, pas d'outil externe : juste un Dockerfile et un script bash.

Vous produirez (à côté des fichiers fournis) :

- Un `Dockerfile`
- Un script de démarrage qui fera office d'`ENTRYPOINT` (lance MariaDB, attend qu'elle réponde, joue le schéma au premier démarrage, puis lance Apache)
- Un `.dockerignore`
- Trois scripts de pilotage : `construire.sh`, `demarrer.sh`, `arreter.sh`
- Un `README.md` qui présente votre travail et explique la persistance des données

Démontrer la persistance fait partie des exigences : ajouter une espèce, arrêter, redémarrer, vérifier qu'elle est toujours là. C'est ce qui valide que votre volume est bien configuré.
