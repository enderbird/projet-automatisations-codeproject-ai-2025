#!/bin/bash
set -e

nom="${1:-Etudiant Inconnu}"
matricule="${2:-0000000}"
date="$(date -I)"

IMAGE="borne-medias-pygame:1.0"

echo "[build] Construction image $IMAGE"

docker build \
  --build-arg NOM_ETUDIANT="$nom" \
  --build-arg MATRICULE="$matricule" \
  --build-arg BUILD_DATE="$date" \
  -t "$IMAGE" .

echo "[ok] Image prête"