# Image officielle Redis
FROM redis:7

# Commande de lancement de Redis
COPY ./config/redis.conf /usr/local/etc/redis/redis.conf

CMD [ "redis-server", "/usr/local/etc/redis/redis.conf", "--appendonly", "yes" ]