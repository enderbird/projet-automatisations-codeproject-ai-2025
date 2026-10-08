#!/bin/bash
set -e

CONTAINER_NAME="borne-vision"

echo "Arrêt de la borne..."

docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true

echo "Borne arrêtée"