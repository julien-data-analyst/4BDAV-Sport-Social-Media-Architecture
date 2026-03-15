# Image officielle PostgreSQL
FROM postgres:16

# Variables d'environnement (peuvent être surchargées dans docker-compose)
ENV POSTGRES_DB=social_media_sports
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres

# Copier le script SQL d'initialisation
COPY ./scripts/create_bdd_social_media_sports.sql /docker-entrypoint-initdb.d/

# PostgreSQL exécutera automatiquement ce script au premier lancement