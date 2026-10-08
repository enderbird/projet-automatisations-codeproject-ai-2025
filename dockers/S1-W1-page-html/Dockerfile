# Image officielle Apache, base Alpine Linux minimale
FROM httpd:alpine

#Étiquettes pour identifier l'image
LABEL pavillon="oiseaux-migrateurs"
LABEL description="Encyclopédie des oiseaux migrateurs du Saint-Laurent"
LABEL version="1.0"

#Copier le contenu du dossier local vers le dossier servi par Apache
COPY contenu/ /usr/local/apache2/htdocs/

#Documenter le port utilisé par Apache
EXPOSE 80
