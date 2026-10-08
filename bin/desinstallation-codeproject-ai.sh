#!/bin/bash
# =============================================================================
# Script de desinstallation de Codeproject.AI
# - Configure : suppression complète du service et nettoyage du système
# - Usage dev : tmp=$(mktemp) && curl -fsSL -H "Cache-Control: no-cache" "https://raw.githubusercontent.com/cegepmatane/projet-automatisations-codeproject-ai/main/bin/desinstallation-codeproject-ai.sh" -o "$tmp" && chmod +x "$tmp" && sudo "$tmp"; rm -f "$tmp"
# =============================================================================
set -e

if [ "$EUID" -ne 0 ]; then
  echo "Ce script doit etre execute avec sudo."
  echo "Exemple : sudo bash desinstallation-codeproject-ai.sh"
  exit 1
fi

echo "============================================================"
echo "  Desinstallation de Codeproject.AI"
echo "============================================================"

echo ""
# -----------------------------------------------------------------------------
# 1. Desactivation des ports
# -----------------------------------------------------------------------------
echo ">>> Etape 1/7 : Configuration du firewall UFW"

ufw delete allow 8080/tcp || true

read -p ">>> Voulez-vous supprimer le port 80 (HTTP) ? [y/N] " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
  ufw delete allow 80/tcp || true
  echo "Port 80 supprime (OK)"
else
  echo "Port 80 conserve (OK)"
fi

ufw status verbose

echo ""
# -----------------------------------------------------------------------------
# 2. Desinstallation unzip
# -----------------------------------------------------------------------------
echo ">>> Etape 2/7 Desinstallation unzip..."

read -p ">>> Voulez-vous desinstaller unzip ? [y/N] " answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
  apt remove -y unzip || true
  echo "unzip desinstalle (OK)"
else
  echo "unzip conserve (OK)"
fi

apt-get update

echo ""
# -----------------------------------------------------------------------------
# 3. Desinstallation .NET 9
# -----------------------------------------------------------------------------
echo ">>> Etape 3/7 : Desinstallation .NET 9"

# Pour pas avoir de conflits
echo "arret du service..."
systemctl stop codeproject.ai-server 2>/dev/null || true
systemctl disable codeproject.ai-server 2>/dev/null || true

apt-get purge -y dotnet-sdk-9.0 || true
apt-get purge -y dotnet-host-9.0 || true
apt-get autoremove -y
yes | add-apt-repository --remove ppa:dotnet/backports || true
apt-get update

if dotnet --version 2>/dev/null; then
  echo "dotnet ENCORE PRESENT (PAS OK)"
  exit 1
else
  echo "dotnet supprimé (OK)"
fi

echo ""
# -----------------------------------------------------------------------------
# 4. Desinstallation de CodeProject.AI-Server
# -----------------------------------------------------------------------------
echo ">>> Etape 4/7 : Desinstallation de CodeProject.AI-Server"

dpkg -r codeproject.ai-server || true

# Dossiers d'installation
rm -rf /usr/bin/codeproject.ai-server-2.9.5
# Données et configuration utilisateur
rm -rf /opt/codeproject/ai 2>/dev/null || true
rm -rf ~/.codeproject 2>/dev/null || true
# Raccourci
rm -f /usr/local/bin/codeproject.ai-server 2>/dev/null || true
# Fichier de service systemd résiduel
rm -f /etc/systemd/system/codeproject.ai-server.service 2>/dev/null || true
systemctl daemon-reload 2>/dev/null || true
# Dossier résiduel du projet
rm -rf /etc/codeproject 2>/dev/null || true

echo "CodeProject.AI-Server desinstalle (OK)"

echo ""
# -----------------------------------------------------------------------------
# 5. Suppression authentification HTTP
# -----------------------------------------------------------------------------
echo ">>> Etape 5/7 : Suppression authentification HTTP"

rm -rf /etc/nginx/codeproject-ai

echo "Configurations authentification HTTP supprime (OK)"

echo ""
# -----------------------------------------------------------------------------
# 6. Suppression configurations Nginx
# -----------------------------------------------------------------------------
echo ">>> Etape 6/7 : Suppression configurations Nginx"

rm -f /etc/nginx/sites-enabled/codeproject-ai
rm -f /etc/nginx/sites-available/codeproject-ai

nginx -t && systemctl restart nginx

echo "Configurations Nginx supprime (OK)"

echo ""
# -----------------------------------------------------------------------------
# 7. Suppression fichier index.html
# -----------------------------------------------------------------------------
echo ">>> Etape 7/7 : Suppression fichier index.html"

rm -rf /var/www/html/codeproject-ai

echo ""
# -----------------------------------------------------------------------------
# DESINSTALLATION TERMINEE (on peut starter le service)
# -----------------------------------------------------------------------------
echo "DESINSTALLATION TERMINEE"