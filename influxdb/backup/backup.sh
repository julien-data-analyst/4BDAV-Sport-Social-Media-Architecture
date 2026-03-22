#!/bin/bash


while true; do
  # Attendre que InfluxDB soit prêt
  echo "Waiting database to be initialized"

  # Test de santé du bdd
  until curl -s http://influxdb_sensors_activity:8086/health | grep -q "pass"; do
    echo "Database not ready, retry in two seconds"
    sleep 2
  done

  echo "Database ready, create the backup"

  # Date et heure d'aujourd'hui
  DATE=$(date +%Y%m%d_%H%M%S)

  influx backup /backup/$DATE \
    --host http://influxdb_sensors_activity:8086 \
    --token my-super-token \
    --org sports_org

  # Message de réussite
  echo "Backup created succesfully : $DATE"

  # rotation (3 jours)
  find /backup -type f -mtime +3 -delete

  sleep 86400 # 24h
done