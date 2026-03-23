# Sujet : Plateforme de gestion d'un réseau social pour sportifs
## Auteur : Julien RENOULT
## Promo : PGE4 Spécialité Data
### *Date : 13/03/2026-23/03/2026*

# Services [PostgreSQL](https://www.postgresql.org/)

Les services ci-dessous nous permettent la création de la base de données historique pour nos capteurs et posts.
PostgreSQL a été un choix évident dû à la grande volumétrie des données à enregistrer avec des requêtes complexes à créer.
Elle nous permettra à l'avenir de proposer des solutions de Big Data analytics et d'aller encore plus loin sur les données récoltées.

# postgres_social_media

Ce premier service permet la création de la base de données en se basant sur quatre fichiers pour l'initialisation :
- **pg_hba.conf :** permets l'utilisation et de pg_dump pour la création de backup 
- **postgresql.conf :** permets la configuration de la base de données en limitant le nombre de connexions par exemple
- **create_bdd_social_media_sports.sql :** permets la création des tables dans la base de données
- **create_role.sql :** permets la création des rôles sur la base de données afin de respecter le principe du *moindre privilège*

# postgresql-bakcup

Ce deuxième service comme son nom l'indique nous permet de 
créer une backup tous les 2 jours afin de sauvegarder les données liées au premier service.
Vous trouverez le script concerné dans le dossier *backup* nommé *backup.sh* qui est exécuté dans ce service.