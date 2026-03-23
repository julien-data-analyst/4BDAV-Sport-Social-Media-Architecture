# Sujet : Plateforme de gestion d'un réseau social pour sportifs
## Auteur : Julien RENOULT
## Promo : PGE4 Spécialité Data
### *Date : 13/03/2026-23/03/2026*

# Services [InfluxDB](https://www.influxdata.com/)

Les services détaillées ci-dessous permettent de mettre en fonctionnement la base de données **InfluxDB**.
Cette base nous servira principalement dans la capture de données par des capteurs mais aussi pour le monitoring de serveur.
Elle est très utile pour de l'analyse en temps réels des performances de l'utilisateur et le calcul des KPIs pour la base de données.

# influxdb_sensors_activity

Ce premier service est celui qui va contenir la base de données.
Elle se basera sur le fichier *config.toml* dans le dossier *config* 
pour configurer la base de données et les variables données en argument dans le docker compose.

# influx-init

Ce deuxième service va être exécuté qu'une seule fois après l'initialisation de la base de données
pour créer les deux tokens nécessaires à la lecture seulement et l'écriture seulement.
Cela permettra de séparer les responsabilités entre les capteurs qui seront dans l'écriture des données 
et les dashboards/workers qui vont lire seulement ces données.

Pour ce qui est de la conservation de ces données, la politique de rétention sera d'une semaine 
et après nous supprimerons les données pour limiter le volume de données.

Vous trouverez le script concerné dans le dossier *initdb*.

# influx-bakcup

Ce dernier service va créer le backup de la base de données tous les 3 jours
et supprimer celles qui datent de plus de 3 jours.
Pourquoi un délai aussi court ? Nous faisons face à des données très volatiles qui n'ont pas grand d'intérêt
à être gardé vu que l'historique des KPIs sera dans la base de données SQL.

Vous trouverez le script concerné dans le dossier *backup* nommé *backup.sh*.

