#!/bin/bash

while true; do
  # Attendre que PostgreSQL soit prêt
  echo "Waiting database to be initialized"

  # Test de santé du bdd
  until pg_isready -h postgres -U postgres; do
    echo "Database not ready, retry in 2s"
    sleep 2
  done

  # Date d'aujourd'hui
  DATE=$(date +%Y%m%d_%H%M%S)

  # connexion au postgre et création backup
  pg_dump -h postgres_social_media -U postgres social_media_sports \
  > /backup/postgres_$DATE.sql

  # rotation (7 jours)
  find /backup -type f -mtime +7 -delete
  
  # Message de réussite
  echo "Backup created : $DATE"

  # S'exécute tous les 2 jours
  sleep 172800  # 2 jours
done