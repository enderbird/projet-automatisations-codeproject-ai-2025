FROM python:3.12-slim

LABEL borne="medias-pygame"

# Dépendances système minimales pour SDL2 / Pygame
RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Pygame
RUN pip install --no-cache-dir pygame==2.5.2

WORKDIR /borne

# Copier le code
COPY option-pygame/application/ /borne/

# Bannières (OBLIGATOIRE)
ARG NOM_ETUDIANT
ARG MATRICULE
ARG BUILD_DATE

ENV NOM_ETUDIANT=$NOM_ETUDIANT
ENV MATRICULE=$MATRICULE
ENV BUILD_DATE=$BUILD_DATE

# Lancer le quiz
CMD ["python", "quiz.py"]