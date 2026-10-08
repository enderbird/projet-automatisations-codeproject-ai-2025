#!/usr/bin/env bash
set -euo pipefail
# =============================================================================
# Script de surveillance de CodeProject.AI
# - Usage : tmp=$(mktemp) && curl -fsSL -H "Cache-Control: no-cache" "https://raw.githubusercontent.com/cegepmatane/projet-automatisations-codeproject-ai/main/bin/surveillance.sh" -o "$tmp" && chmod +x "$tmp" && sudo "$tmp"; rm -f "$tmp"
#
# =============================================================================

readonly NOM_SERVICE="codeproject.ai-server"

readonly DOSSIER_AUDIT="/root/audit"
readonly SUFFIXE="$(tr -dc 'a-z0-9' < /dev/urandom | head -c 4)"
readonly FICHIER_AUDIT="${DOSSIER_AUDIT}/audit-$(date +%Y-%m-%d)-${SUFFIXE}.txt"

mkdir -p "${DOSSIER_AUDIT}"

echo "===== AUDIT ${NOM_SERVICE} $(date) =====" | tee -a "${FICHIER_AUDIT}"

echo ""
echo ">>> 1. Service systemd" | tee -a "${FICHIER_AUDIT}"
systemctl is-active "${NOM_SERVICE}" | tee -a "${FICHIER_AUDIT}"

echo ""
echo ">>> 2. Port 8080 (nginx)" | tee -a "${FICHIER_AUDIT}"
ss -tlnp | grep ":8080" | tee -a "${FICHIER_AUDIT}" || echo "PORT 8080 ABSENT" | tee -a "${FICHIER_AUDIT}"

echo ""
echo ">>> 3. RAM" | tee -a "${FICHIER_AUDIT}"
free -h | awk '/Mem:/ {print "RAM libre:", $7}' | tee -a "${FICHIER_AUDIT}"

echo ""
echo ">>> 4. Disque" | tee -a "${FICHIER_AUDIT}"
df -h / | awk 'NR==2 {print "Disque libre:", $4, "utilisé:", $5}' | tee -a "${FICHIER_AUDIT}"

echo ""
echo ">>> 5. Nginx status" | tee -a "${FICHIER_AUDIT}"
systemctl is-active nginx | tee -a "${FICHIER_AUDIT}"

echo ""
echo ">>> 6. Test API" | tee -a "${FICHIER_AUDIT}"

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/)

echo "HTTP CODE: $HTTP_CODE" | tee -a "${FICHIER_AUDIT}"

if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 401 ]; then
    echo "API OK (service up)" | tee -a "${FICHIER_AUDIT}"
else
    echo "API FAIL" | tee -a "${FICHIER_AUDIT}"
fi

echo ""
echo "AUDIT TERMINÉ"