#!/bin/sh

echo "Waiting Grafana to be ready"

# Test de santé pour Grafana
until wget -q -O - http://grafana-dashboard-sensor-monitoring:3000/api/health | grep -q "ok"; do
  echo "Grafana not ready, retry in 2s"
  sleep 2
done

echo "Grafana is ready, backup creation"

# Création du backup
while true; do
  DATE=$(date +%Y%m%d_%H%M%S)

  # Essayer de créer le backup, sinon on retourne failed
  if tar -czf /backup/grafana_$DATE.tar.gz /var/lib/grafana; then
    echo "Backup Grafana OK : $DATE"
  else
    echo "Backup Grafana FAILED : $DATE"
  fi

  # rotation (7 jours)
  find /backup -type f -mtime +7 -delete

  sleep 86400 # 24 h
done