#!/bin/bash
set -e

IMAGE_NAME="borne-vision:1.0"
CONTAINER_NAME="borne-vision"

echo "Activation X11..."
xhost +local:docker

echo "Lancement du container..."

# stop si déjà existant
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

docker run -d \
  --name "$CONTAINER_NAME" \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  "$IMAGE_NAME"

echo "Borne démarrée"
echo "xLogs : docker logs -f $CONTAINER_NAME"