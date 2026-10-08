#!/usr/bin/env bash
set -euo pipefail

# =============================================================================
# Script d'installation de CodeProject.AI
# - Configure : installation complète du service (paquet, config nginx, service systemd, port, webclient)
# - Usage dev : tmp=$(mktemp) && curl -fsSL -H "Cache-Control: no-cache" "https://raw.githubusercontent.com/cegepmatane/projet-automatisations-codeproject-ai/main/bin/installation-codeproject-ai.sh" -o "$tmp" && chmod +x "$tmp" && sudo "$tmp"; rm -f "$tmp"
#
# =============================================================================

# =============================================================================
# VARIABLES
# =============================================================================

readonly NOM_SERVICE="codeproject.ai-server"
readonly VERSION_CODEPROJECT="2.9.5"

readonly BUILD_HASH="$(git rev-parse --short HEAD 2>/dev/null || echo 'sans-git')"
readonly BUILD_DATE="$(date +%Y-%m-%d)"

readonly SERVER_IP="$(hostname -I | awk '{print $1}')"

readonly INSTALL_DIR="/usr/bin/codeproject.ai-server-${VERSION_CODEPROJECT}"

readonly PACKAGE_NAME="codeproject.ai-server_${VERSION_CODEPROJECT}_Ubuntu_x64"

readonly PACKAGE_URL="https://codeproject-ai-bunny.b-cdn.net/server/installers/linux/${PACKAGE_NAME}.zip"

# =============================================================================
# BANNIERE
# =============================================================================

banniere() {
    echo "============================================================"
    echo "BUILD ${BUILD_HASH} ${BUILD_DATE}"
    echo "Installation CodeProject.AI"
    echo "============================================================"
}

banniere

# =============================================================================
# VALIDATION ROOT
# =============================================================================

if [ "$(id -u)" -ne 0 ]; then
    echo "ERREUR : executer avec sudo"
    exit 1
fi

# =============================================================================
# ETAPE 1 - FIREWALL
# =============================================================================

echo ""
echo ">>> Etape 1/8 : Firewall"

apt-get update

DEBIAN_FRONTEND=noninteractive apt-get install -y ufw

ufw allow 80/tcp
ufw allow 8080/tcp

ufw --force enable

echo "Verification firewall"
ufw status verbose

# =============================================================================
# ETAPE 2 - DEPENDANCES
# =============================================================================

echo ""
echo ">>> Etape 2/8 : Dependances"

DEBIAN_FRONTEND=noninteractive apt-get install -y \
    software-properties-common \
    unzip \
    wget \
    curl \
    nginx \
    apache2-utils

echo "Verification curl"
curl --version | head -n 1

# =============================================================================
# ETAPE 3 - .NET 9
# =============================================================================

echo ""
echo ">>> Etape 3/8 : .NET 9"

if ! add-apt-repository -y ppa:dotnet/backports; then
  echo "WARNING: PPA déjà présent ou erreur mineure (continuing)"
fi

apt-get update

DEBIAN_FRONTEND=noninteractive apt-get install -y dotnet-sdk-9.0

echo "Verification .NET"
dotnet --version

# =============================================================================
# ETAPE 4 - TELECHARGEMENT
# =============================================================================

echo ""
echo ">>> Etape 4/8 : Telechargement"

wget -O "${PACKAGE_NAME}.zip" "${PACKAGE_URL}"

echo "Verification archive"
ls -lh "${PACKAGE_NAME}.zip"

# =============================================================================
# ETAPE 5 - INSTALLATION CODEPROJECT.AI
# =============================================================================

echo ""
echo ">>> Etape 5/8 : Installation"

unzip -o "${PACKAGE_NAME}.zip"

rm -f "${PACKAGE_NAME}.zip"

dpkg -i "${PACKAGE_NAME}.deb" || apt --fix-broken install -y

rm -f "${PACKAGE_NAME}.deb"

pushd "${INSTALL_DIR}" > /dev/null
bash setup.sh
popd > /dev/null

pushd "${INSTALL_DIR}/server" > /dev/null
bash ../setup.sh
popd > /dev/null

systemctl enable "${NOM_SERVICE}"

echo "Verification service"
systemctl is-enabled "${NOM_SERVICE}"

# =============================================================================
# ETAPE 6 - AUTH NGINX
# =============================================================================

echo ""
echo ">>> Etape 6/8 : Auth nginx"

mkdir -p /etc/nginx/codeproject-ai

# NOTE :
# Exemple automatisable :
# export ADMIN_PASSWORD="motdepasse"
# htpasswd -b -c /etc/nginx/codeproject-ai/.htpasswd admin "$ADMIN_PASSWORD"

if [ -z "${ADMIN_PASSWORD:-}" ]; then
    read -s -p "Mot de passe admin: " ADMIN_PASSWORD
    echo
fi

htpasswd -b -c /etc/nginx/codeproject-ai/.htpasswd admin "$ADMIN_PASSWORD"

chmod 640 /etc/nginx/codeproject-ai/.htpasswd

chown root:www-data /etc/nginx/codeproject-ai/.htpasswd

echo "Verification htpasswd"
ls -l /etc/nginx/codeproject-ai/.htpasswd

# =============================================================================
# ETAPE 7 - CONFIGURATION NGINX
# =============================================================================

echo ""
echo ">>> Etape 7/8 : Configuration nginx"

cat > /etc/nginx/sites-available/codeproject-ai << EOF
limit_req_zone \$binary_remote_addr zone=limite_adresses:10m rate=10r/s;

server {
    listen 80;
    server_name ${SERVER_IP};

    limit_req zone=limite_adresses burst=20 nodelay;

    client_max_body_size 20M;

    location /codeproject-ai/ {
        root /var/www/html;
        index index.html;
    }

    location /codeproject-api/ {
        proxy_pass http://127.0.0.1:32168/;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

        proxy_http_version 1.1;

        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}

server {
    listen 8080;
    server_name ${SERVER_IP};

    limit_req zone=limite_adresses burst=20 nodelay;

    client_max_body_size 20M;

    auth_basic "Admin Only";
    auth_basic_user_file /etc/nginx/codeproject-ai/.htpasswd;

    location / {
        proxy_pass http://127.0.0.1:32168/;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;

        proxy_http_version 1.1;

        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
EOF

ln -sf \
/etc/nginx/sites-available/codeproject-ai \
/etc/nginx/sites-enabled/codeproject-ai

echo "Verification nginx config"

nginx -t

systemctl restart nginx

# =============================================================================
# ETAPE 8 - WEBCLIENT
# =============================================================================

echo ""
echo ">>> Etape 8/8 : Webclient"

mkdir -p /var/www/html/codeproject-ai

cat > /var/www/html/codeproject-ai/index.html << EOF
<html>
  <body>
    Detecter la scene dans ce fichier:
    <input id="image" type="file" />
    
    <input type="button" value="Detect Scene" onclick="detectScene(image)" />
    
    <script>
      function detectScene(fileChooser) {
        var formData = new FormData();
      
        formData.append('image', fileChooser.files[0]);
      
        fetch('http://${SERVER_IP}/codeproject-api/v1/vision/detection', {
          method: "POST",
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          console.log(data);
      
          const pred = data.predictions?.[0];
          if (pred) {
            console.log(pred.label, pred.confidence);
          }
        });
      }
    </script>
  </body>
</html>
EOF

# =============================================================================
# DEMARRAGE
# =============================================================================

echo ""
echo ">>> Demarrage"

systemctl start "${NOM_SERVICE}"

# =============================================================================
# OPTIMISATION
# =============================================================================

echo ""
echo ">>> Optimisation"

sed -i \
'0,/"AutoStart": true/s//"AutoStart": false/' \
"${INSTALL_DIR}/modules/FaceProcessing/modulesettings.json" \
2>/dev/null || true

sed -i \
'0,/"AutoStart": true/s//"AutoStart": false/' \
"${INSTALL_DIR}/modules/ObjectDetectionYOLOv5Net/modulesettings.json" \
2>/dev/null || true

rm -rf "${INSTALL_DIR}/modules/FaceProcessing" || true

rm -rf "${INSTALL_DIR}/modules/ObjectDetectionYOLOv5Net" || true

# =============================================================================
# VERIFICATIONS FINALES
# =============================================================================

echo ""
echo ">>> Verifications finales"

echo "Verification service actif"
systemctl is-active "${NOM_SERVICE}"

echo "Verification port 8080"
ss -tlnp | grep ":8080"

echo "Verification webclient"
curl -fsS \
"http://localhost:8080/" \
> /dev/null && echo "OK"

# =============================================================================
# FIN
# =============================================================================

echo ""
echo "============================================================"
echo "INSTALLATION TERMINEE"
echo "============================================================"

echo "Dashboard : http://${SERVER_IP}:8080"
echo "Webclient : http://${SERVER_IP}/codeproject-ai/"
echo ""