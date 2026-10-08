#!/bin/bash
set -e

docker stop borne-accueil || true
docker rm borne-accueil || true