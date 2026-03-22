#!/bin/sh

# Utilisation du .env afin de récupérer les utilisateurs et mots de passes 
sed -e "s|\${REDIS_PASSWORD_ADMIN}|$REDIS_PASSWORD_ADMIN|g" \
    -e "s|\${REDIS_USER_ADMIN}|$REDIS_USER_ADMIN|g" \
    -e "s|\${REDIS_USER_SM}|$REDIS_USER_SM|g" \
    -e "s|\${REDIS_PASSWORD_SM}|$REDIS_PASSWORD_SM|g" \
    -e "s|\${REDIS_USER_SENSOR}|$REDIS_USER_SENSOR|g" \
    -e "s|\${REDIS_PASSWORD_SENSOR}|$REDIS_PASSWORD_SENSOR|g" \
    -e "s|\${REDIS_WORKER}|$REDIS_WORKER|g" \
    -e "s|\${REDIS_PASSWORD_WORKER}|$REDIS_PASSWORD_WORKER|g" \
    /redis.conf.template > /redis.conf

# Lancement du serveur avec la config de créée
redis-server /redis.conf