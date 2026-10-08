#!/usr/bin/env bash
set -euo pipefail

readonly NOM_SERVICE="codeproject.ai-server"

readonly DOSSIER_BACKUP="/root/backups/${NOM_SERVICE}"
readonly DATE_HORO="$(date +%Y-%m-%d_%H-%M)"
readonly ARCHIVE="${NOM_SERVICE}-${DATE_HORO}.tar.gz"

# dossiers probables (ajuste si besoin)
readonly DATA_DIR="/var/lib/${NOM_SERVICE}"
readonly NGINX_DIR="/etc/nginx/codeproject-ai"

echo "===== BACKUP ${NOM_SERVICE} ${DATE_HORO} ====="

mkdir -p "${DOSSIER_BACKUP}"

echo ">>> Création archive..."

tar -czf "${DOSSIER_BACKUP}/${ARCHIVE}" \
    "${DATA_DIR}" \
    "${NGINX_DIR}" \
    /var/www/html/codeproject-ai \
    /etc/nginx/sites-available/codeproject-ai \
    /etc/nginx/sites-enabled/codeproject-ai \
    2>/dev/null || true

echo ">>> Rotation (garde 7 jours)"

find "${DOSSIER_BACKUP}" \
    -name "${NOM_SERVICE}-*.tar.gz" \
    -mtime +7 \
    -delete

echo "BACKUP OK : ${ARCHIVE}"