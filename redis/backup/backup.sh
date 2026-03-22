#!/bin/bash

while true; do

  # Attendre que Redis soit prêt
  until redis-cli -h redis_social_media -a myStrongPassword --user admin ping | grep -q PONG; do
    echo "Redis is not ready, retry in 2s"
    sleep 2
  done

  # Création du backup redis
  DATE=$(date +%Y%m%d_%H%M%S)

  # attendre la fin de la sauvegarde

  ## Capturer la dernière backup avant celui-là)
  LAST=$(redis-cli -h redis_social_media -a myStrongPassword --user admin LASTSAVE)

  # Création du backup
  redis-cli -h redis_social_media -a myStrongPassword --user admin BGSAVE

  ## Attendre que notre nouvelle sauvegarde soit terminée
  while [ "$LAST" -eq "$(redis-cli -h redis_social_media -a myStrongPassword --user admin LASTSAVE)" ]; do
    sleep 1
  done

  sleep 3

  # déplacer le backup redis
  cp /backup_data/dump.rdb ./backup_data/redis_$DATE.rdb

  # Mettre un message de confirmation du backup
  echo "Redis backup created : redis_$DATE.rdb"

  # rotation (2 jours)
  find /backup_data -type f -mtime +2 -delete

  sleep 86400  # 24h

done