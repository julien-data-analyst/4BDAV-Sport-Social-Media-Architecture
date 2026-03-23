#!/bin/bash

export INFLUX_TOKEN=$INFLUX_TOKEN
export INFLUX_ORG=$INFLUX_ORG
export INFLUX_HOST=http://influxdb_sensors_activity:8086

# Attendre que la base de données soit prête
echo "Waiting for InfluxDB to start"

until curl -s http://influxdb_sensors_activity:8086/health | grep -q '"status":"pass"'; do
  sleep 2
done

echo "InfluxDB is ready, create the tokens"

export BUCKET_ID=$(influx bucket ls --hide-headers --name sports_metrics | cut -f1)

# Création du token pour lecture des activités seulement (dashboard + workers)
influx auth create \
  --org "$INFLUX_ORG" \
  --read-bucket $BUCKET_ID \
  --description "read-only activities"

# Création du token pour écriture des activités seulement (capteurs)
influx auth create \
  --org "$INFLUX_ORG" \
  --write-bucket $BUCKET_ID \
  --description "sensor writer for activities"

echo "Tokens read-only and write-only created"