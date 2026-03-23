# Sujet : Plateforme de gestion d'un réseau social pour sportifs
## Auteur : Julien RENOULT
## Promo : PGE4 Spécialité Data
### *Date : 13/03/2026-23/03/2026*

# Services [Redis](https://redis.io/)

Les deux services ci-dessous permettent la création de la base de données **Redis** et du backup.
La base de données Redis va servir principalement à la capture de données du réseau social 
en profitant de sa rapiditié d'écriture et de sa simplicité pour aller chercher les données.
De plus, un système Pub/Sub sera utilisé pour le follow d'autre personnes ce qui est simplifiée par ce type de base.
Nous pouvons rajouter l'utilité de son système de cache pour la 
partie des capteurs afin d'identifier les nouvelles activités 
qui ne sont pas encore insérées dans la base de données.


# redis_social_media

Ce premier service permet la création de la base de données 
en se basant sur deux fichiers pour l'initialisation :
- **redis.conf.template :** template pour la configurationd de la base Redis, c'est ici qu'on créera les différents utilisateurs
- **entrypoint.sh :** un script bash qui va utiliser et remplir le template via les variables d'environnements et démarrer le serveur avec la configuration résultante

# redis-bakcup

Ce deuxième service comme son nom l'indique nous permet de 
créer une backup tous les 24 heures afin de sauvegarder les données liées au premier service.
Ce délais court est faits exprès car nous faisons face à des données très volatiles ce qui nécessite de sauvegarder assez souvent la base de données.
Vous trouverez le script concerné dans le dossier *backup* nommé *backup.sh* qui est exécuté dans ce service.