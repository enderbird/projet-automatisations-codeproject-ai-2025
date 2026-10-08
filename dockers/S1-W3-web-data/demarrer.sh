#!/bin/bash
set -e

#Chemins
cheminFichierTemoin="/var/lib/mysql/initialise.flag"
cheminSchema="/docker-entree/schema.sql"

#Couleurs ANSI
BLEU="\033[1;34m"
VERT="\033[1;32m"
JAUNE="\033[1;33m"
RESET="\033[0m"

#1. Démarrer MariaDB en arrière-plan
echo -e "${BLEU}[info]${RESET} Démarrage de MariaDB..."
service mariadb start

#2. Attendre que MariaDB soit prête
echo -e "${BLEU}[info]${RESET} Attente que MariaDB soit prête..."
until mysqladmin ping -h localhost --silent; do
    echo -e "${JAUNE}[...] ${RESET} MariaDB pas encore prête, nouvelle tentative dans 1 s..."
    sleep 1
done
echo -e "${VERT}[ok]${RESET} MariaDB répond."

#3. Premier démarrage : jouer le schéma SQL
if [ ! -f "$cheminFichierTemoin" ]; then
    echo -e "${BLEU}[info]${RESET} Initialisation du schéma (premier démarrage)..."
    mysql < "$cheminSchema"
    touch "$cheminFichierTemoin"
    echo -e "${VERT}[ok]${RESET} Schéma initialisé. 12 espèces chargées."
else
    echo -e "${VERT}[ok]${RESET} Schéma déjà initialisé, on saute."
fi

mysql <<EOF
CREATE USER IF NOT EXISTS 'catalogue_app'@'localhost' IDENTIFIED BY 'pavillon-bsl';
GRANT ALL PRIVILEGES ON catalogue_especes.* TO 'catalogue_app'@'localhost';
FLUSH PRIVILEGES;
EOF

#4. Lancer Apache en avant-plan (devient le PID 1 du container)
echo -e "${BLEU}[info]${RESET} Lancement d'Apache en avant-plan..."
exec apache2-foreground