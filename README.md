# Cédric Simard
projet-automatisations...

## [Feuille Synthèse](https://1drv.ms/w/c/b850b47cdbccabb1/IQD7YbWTu1s9TakNjQXnIlGhAWu0qbTND_UmNBKJ9o9Sk4g?e=dZ7nBQ)...

## NOTE : 
Par exemple, les pages vont être http://192.46.222.166:8080 et http://192.46.222.166/codeproject-ai/. Aussi, le contenu de http://192.46.222.166/index.html devrait être accessible même après l'installation.


## Script d'installation de CodeProject.AI :
- Configure : installation complète du service (paquet, config nginx, service systemd, port, webclient)
- Usage : 
```bash
tmp=$(mktemp) && curl -fsSL "https://raw.githubusercontent.com/cegepmatane/projet-automatisations-codeproject-ai/main/bin/installation-codeproject-ai.sh" -o "$tmp" && chmod +x "$tmp" && sudo "$tmp"; rm -f "$tmp"
```
ou directement entrer le mot passe de nginx pour la page avec l'utilisateur "admin" sur le navigateur:
```bash
export ADMIN_PASSWORD="VotreMotDePasseSemiSecurise" && tmp=$(mktemp) && curl -fsSL "https://raw.githubusercontent.com/cegepmatane/projet-automatisations-codeproject-ai/main/bin/installation-codeproject-ai.sh" -o "$tmp" && chmod +x "$tmp" && sudo "$tmp" && rm -f "$tmp"
```

### BONUS : Script de desinstallation de Codeproject.AI :
- Configure : suppression complète du service et nettoyage du système
- Usage : 
```bash
tmp=$(mktemp) && curl -fsSL "https://raw.githubusercontent.com/cegepmatane/projet-automatisations-codeproject-ai/main/bin/desinstallation-codeproject-ai.sh" -o "$tmp" && chmod +x "$tmp" && sudo "$tmp"; rm -f "$tmp"
```

## Script de sauvegarde :
Voir la dernière backups si elle a fonctionnée:
- Usage :
   - Installation automatique backups :
```bash
sudo curl -fsSL "https://raw.githubusercontent.com/cegepmatane/projet-automatisations-codeproject-ai/main/bin/sauvegarde.sh" -o /usr/local/bin/sauvegarde.sh && sudo chmod +x /usr/local/bin/sauvegarde.sh && (crontab -l 2>/dev/null | grep -v "sauvegarde.sh" ; echo "0 2 * * * bash /usr/local/bin/sauvegarde.sh >> /root/audit/backup.log 2>&1") | crontab -
```
   - **BONUS** : Desinstallation : 
```bash
(crontab -l 2>/dev/null | grep -v "sauvegarde.sh" | crontab -) && sudo rm -f /usr/local/bin/sauvegarde.sh
```
> \> **NOTE** :
>Pour valider si installé (ou désinstallé) : 
>```bash
>crontab -l
>```
   - Voir toutes les backups triées par date :
```bash
sudo ls -lt /root/backups/codeproject.ai-server
```
   - Voir la dernière backup :
```bash
sudo tar -tzf "$(sudo find /root/backups/codeproject.ai-server -name '*.tar.gz' | head -n 1)" | head
```

## Script de surveillance :
- Usage :
```bash
tmp=$(mktemp) && curl -fsSL "https://raw.githubusercontent.com/cegepmatane/projet-automatisations-codeproject-ai/main/bin/surveillance.sh" -o "$tmp" && chmod +x "$tmp" && sudo "$tmp"; rm -f "$tmp"
```

- Voir dernières logs :
```bash
sudo bash -c 'cat "$(ls -t /root/audit/*.txt | head -n 1)"'
```
