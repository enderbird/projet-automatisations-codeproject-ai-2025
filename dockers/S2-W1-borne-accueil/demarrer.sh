#!/bin/bash
set -e

docker run -d \
  --name borne-accueil \
  -p 8090:3000 \
  zoo-borne-accueil:1.0