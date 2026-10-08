# Image officielle PHP 8.2 avec Apache intégré
FROM php:8.2-apache

LABEL pavillon="catalogue-especes"
LABEL description="Bestiaire des espèces du zoo - PHP + Apache + MariaDB tout-en-un"
LABEL version="1.0"

ENV DEBIAN_FRONTEND=noninteractive

#Installer MariaDB et activer l'extension PDO MySQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        mariadb-server \
        mariadb-client \
    && docker-php-ext-install pdo pdo_mysql \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#Copier l'application PHP à la racine servie par Apache
COPY application/ /var/www/html/

#Copier le schéma SQL dans un dossier dédié (hors de la racine web)
RUN mkdir -p /docker-entree
COPY schema.sql /docker-entree/schema.sql

#Copier le script d'orchestration et le rendre exécutable
COPY demarrer.sh /usr/local/bin/demarrer.sh
RUN chmod +x /usr/local/bin/demarrer.sh

#Préparer le dossier de données MariaDB avec les bons droits
RUN mkdir -p /var/lib/mysql && chown -R mysql:mysql /var/lib/mysql

EXPOSE 80

ENTRYPOINT ["/usr/local/bin/demarrer.sh"]