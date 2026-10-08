#!/bin/bash
set -e

#Variables
nomImage="zoo-pavillon-oiseaux:1.0"
nomContainer="zoo-oiseaux-en-marche"
portHote="8000"
portContainer="80"

#Couleurs ANSI
BLEU="\033[1;34m"
JAUNE="\033[1;33m"
VERT="\033[1;32m"
RESET="\033[0m"

#Nettoyage préventif
# Si un container du même nom existe (arrêté ou actif), le retirer
if docker ps -a --format '{{.Names}}' | grep -q "^${nomContainer}$"; then
  echo -e "${JAUNE}[info]${RESET} Container existant détecté, nettoyage..."
  docker stop "${nomContainer}" 2>/dev/null || true
  docker rm "${nomContainer}"
  echo -e "${JAUNE}[info]${RESET} Ancien container retiré."
fi

#Démarrage
echo -e "${BLEU}[info]${RESET} Démarrage du container ${nomContainer}..."

docker run \
  -d \
  --name "${nomContainer}" \
  -p "${portHote}:${portContainer}" \
  "${nomImage}"

echo -e "${VERT}[ok]${RESET} Encyclopédie disponible à http://localhost:${portHote}/"
echo -e "${VERT}[ok]${RESET} Logs : docker logs ${nomContainer}"
