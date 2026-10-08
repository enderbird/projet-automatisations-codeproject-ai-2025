#!/bin/bash
set -e

#Variables
nomContainer="zoo-oiseaux-en-marche"

#Couleurs ANSI
BLEU="\033[1;34m"
JAUNE="\033[1;33m"
VERT="\033[1;32m"
RESET="\033[0m"

#Vérification
if ! docker ps -a --format '{{.Names}}' | grep -q "^${nomContainer}$"; then
  echo -e "${JAUNE}[info]${RESET} Aucun container nommé '${nomContainer}' trouvé. Rien à faire."
  exit 0
fi

#Arrêt
echo -e "${BLEU}[info]${RESET} Arrêt du container ${nomContainer}..."
docker stop "${nomContainer}"

#Suppression
echo -e "${BLEU}[info]${RESET} Suppression du container..."
docker rm "${nomContainer}"

echo -e "${VERT}[ok]${RESET} Container '${nomContainer}' arrêté et supprimé."
