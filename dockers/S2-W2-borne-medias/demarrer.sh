#!/bin/bash

IMAGE="borne-medias-pygame:1.0"
CONTAINER="borne-medias-pygame"

echo "[run] Lancement du container"

# cleanup automatique (évite conflits)
docker rm -f "$CONTAINER" 2>/dev/null || true

if command -v xhost >/dev/null 2>&1; then
  xhost +local:docker
else
  echo "[warn] xhost introuvable"
fi

docker run -d \
  --name "$CONTAINER" \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  "$IMAGE"

echo "[ok] Borne démarrée"