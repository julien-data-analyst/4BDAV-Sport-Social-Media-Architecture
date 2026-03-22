#!/bin/bash

# Création du token pour lecture des activités seulement (dashboard + workers)
influx auth create \
  --org sports_org \
  --read-bucket sports_metrics \
  --description "read-only activities"

# Création du token pour écriture des activités seulement (capteurs)
influx auth create \
  --org sports_org \
  --write-bucket sports_metrics \
  --description "sensor writer"

