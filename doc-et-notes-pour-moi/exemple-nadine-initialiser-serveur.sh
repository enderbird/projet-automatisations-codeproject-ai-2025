#!/bin/bash
# =============================================================================
# Script d'initialisation serveur pour les etudiants
# Configure : sudoer, UFW (firewall), fail2ban
# Usage : sudo bash initialiser-serveur.sh [nom-usager]
# =============================================================================

set -e

if [ "$EUID" -ne 0 ]; then
  echo "Ce script doit etre execute avec sudo."
  echo "Exemple : sudo bash initialiser-serveur.sh nadine"
  exit 1
fi

nomUsager="${1:-nadine}"

echo "============================================================"
echo "  Initialisation du serveur"
echo "  Usager a creer : $nomUsager"
echo "============================================================"
echo ""

# -----------------------------------------------------------------------------
# 1. Creation de l'usager et ajout au groupe sudo
# -----------------------------------------------------------------------------
echo ">>> Etape 1/4 : Creation de l'usager $nomUsager"
if id "$nomUsager" &>/dev/null; then
  echo "L'usager $nomUsager existe deja, on saute la creation."
else
  adduser "$nomUsager"
fi
usermod -aG sudo "$nomUsager"
echo "Usager $nomUsager ajoute au groupe sudo."
echo ""

# -----------------------------------------------------------------------------
# 2. Installation et configuration de UFW (firewall)
# -----------------------------------------------------------------------------
echo ">>> Etape 2/4 : Configuration du firewall UFW"
apt-get update
apt-get install -y ufw
ufw --force reset
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
ufw status verbose
echo ""

# -----------------------------------------------------------------------------
# 3. Installation de jed (editeur de texte)
# -----------------------------------------------------------------------------
echo ">>> Etape 3/4 : Installation de jed"
apt-get install -y jed
echo ""

# -----------------------------------------------------------------------------
# 4. Installation et configuration de fail2ban
# -----------------------------------------------------------------------------
echo ">>> Etape 4/4 : Installation et configuration de fail2ban"
apt-get install -y fail2ban

# Copie de sauvegarde du fichier de configuration original
if [ ! -f /etc/fail2ban/jail.conf.copie ]; then
  cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.conf.copie
  echo "Copie de sauvegarde creee : /etc/fail2ban/jail.conf.copie"
fi

# On utilise jail.local (methode officielle recommandee) pour ne pas
# modifier jail.conf directement. Les valeurs de jail.local ecrasent
# celles de jail.conf.
cat > /etc/fail2ban/jail.local <<'FIN_CONFIGURATION'
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 5
findtime = 300
bantime = 28800
FIN_CONFIGURATION

echo "Configuration fail2ban ecrite dans /etc/fail2ban/jail.local"

systemctl restart fail2ban
systemctl enable fail2ban.service

echo ""
echo "Statut de fail2ban :"
systemctl is-active fail2ban && echo "fail2ban est actif."

echo ""
echo "============================================================"
echo "  Initialisation terminee avec succes !"
echo "============================================================"
echo ""
echo "Rappel :"
echo "  - Usager cree : $nomUsager (dans le groupe sudo)"
echo "  - Firewall UFW actif : ports 22, 80, 443 ouverts"
echo "  - fail2ban actif : 5 tentatives / 5 min -> ban de 8h"
echo ""
echo "Pour voir les bannissements : sudo fail2ban-client status sshd"
