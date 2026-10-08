#!/bin/bash
set -e

#Variables
nomImage="zoo-evenements"
tagVersion="1.0"

#Couleurs ANSI
BLEU="\033[1;34m"
VERT="\033[1;32m"
RESET="\033[0m"

#Construction
echo -e "${BLEU}[info]${RESET} Construction de l'image ${nomImage}:${tagVersion}..."
echo -e "${BLEU}[info]${RESET} (Premier build : téléchargement de php:8.2-apache ~400 Mo, patientez)"

docker build \
  -t "${nomImage}:${tagVersion}" \
  -t "${nomImage}:latest" \
  .

echo -e "${VERT}[ok]${RESET} Image construite : ${nomImage}:${tagVersion}"
echo -e "${VERT}[ok]${RESET} Vérifiez avec : docker images ${nomImage}"
