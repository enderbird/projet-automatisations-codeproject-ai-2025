#!/bin/bash
set -e

IMAGE_NAME="borne-vision:1.0"

echo "Build de l'image Docker..."

docker build \
  -t "$IMAGE_NAME" \
  .

echo "Build terminé : $IMAGE_NAME"