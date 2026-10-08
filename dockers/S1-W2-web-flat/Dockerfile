#Image officielle PHP 8.2 avec Apache intégré
FROM php:8.2-apache

#Étiquettes pour identifier l'image
LABEL pavillon="evenements"
LABEL description="Mini-CMS flat-file des rendez-vous du zoo"
LABEL version="1.0"

#Copier le moteur PHP à la racine servie par Apache
# (le contenu de moteur/, pas le dossier lui-même)
COPY moteur/ /var/www/html/

#Copier le contenu à côté de index.php, là où le moteur le cherche
# moteur/index.php attend fp-content/ au même niveau que lui
COPY fp-content/ /var/www/html/fp-content/

#Documenter le port utilisé par Apache
EXPOSE 80
