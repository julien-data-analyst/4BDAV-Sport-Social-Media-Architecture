# Sujet : Plateforme de gestion d'un réseau social pour sportifs
## Auteur : Julien RENOULT
## Promo : PGE4 Spécialité Data
### *Date : 13/03/2026-23/03/2026*

# Services [Grafana](https://cloudinary.com/)

Ce service va permettre facilement l'analyse des performances de l'utilisateur mais aussi du monitoring.
Grâce à ses nombreuses connecteurs possibles et aux possibilités de créer plusieurs tableau de bords, 
cela fait un choix essentiel dans notre architecture complexe.

# grafana-dashboard-sensor-monitoring

Ce premier service permet de se connecter au logiciel facilement via 
les variables d'environnements que nous avons renseignées.
Si nous voulons importer des dashboards ou connexions aux bases de données, 
nous pouvons utiliser les dossiers *dashboard et datasources*.
Ces dossiers contiendront les dashboard réalisés et les connexions aux différentes sources
via des fichiers JSON et YML.

# grafana-bakcup

Ce deuxième service comme son nom l'indique nous permet de 
créer une backup toutes les 24 heures afin de sauvegarder les données liées au premier service.
Vous trouverez le script concerné dans le dossier *backup* nommé *backup.sh* qui est exécuté dans ce service.
