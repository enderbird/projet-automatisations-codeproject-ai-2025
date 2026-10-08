#!/bin/bash

CONTAINER="borne-medias-pygame"

echo "[stop] Arrêt du container"

docker stop "$CONTAINER" 2>/dev/null || true
docker rm "$CONTAINER" 2>/dev/null || true

# sécurise xhost
if command -v xhost >/dev/null 2>&1; then
  xhost -local:docker
else
  echo "[warn] xhost introuvable (ignoré)"
fi

echo "[ok] Borne arrêtée"