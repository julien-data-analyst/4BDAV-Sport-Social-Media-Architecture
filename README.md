# Sujet : Plateforme de gestion d'un réseau social pour sportifs
## Auteur : Julien RENOULT
## Promo : PGE4 Spécialité Data
### *Date : 13/03/2026-23/03/2026*

# Introduction

Vous trouverez sous cette documentation comment lancer l'architecture et 
comment générer les données fictives dans les bases de données. 
Si vous voulez lire la documentation technique concernant cette solution, 
vous pouvez vous redirigez vers le fichier *documentation_technique.md* qui expliquera en détail l'architecture proposée.

# Pré-requis 

Pour pouvoir lancer ce projet, il faut bien sûr avoir de docker d'installée :
- [Docker Desktop](https://docs.docker.com/get-started/get-docker/)

Après installation de Docker, vous pourrez utiliser ce projet.

# Lancement de l'architecture

Pour lancer l'architecture, vous devez utiliser la commande ci-dessous :
```sh
docker compose -f docker-compose-dev.yaml up --build -d
```

Cela créera les images et lancera les différents services dont les backups.

# Génération des données fictives

Si vous voulez générer des données fictives après que tous soient créées, 
aller sur l'application marimo de l'adresse suivante 

Vous trouverez un script marimo nommé *generation_data.py* 
qui va générer les données fictives pour les différentes bases de données.

Lancer ce notebook et exécuter-le afin de générer des données fictives, 
vous trouverez des commentaires et des explications sur la génération de ces données fictives et pourquoi.

# Observation des données fictives

Pour observer ces données fictives comment elles se comportent, 
vous pouvez les observer à travers le notebook *visualization_data.py*.
Ce notebook offre un petit aperçu des données que vous avez généré précedemment dans la base de données.

# Aller plus en détail

Si vous voulez comprendre en détail ce que fait chaque service, 
vous trouverez un README sur chacun de ces services expliquant comment elle marche et ce qui est proposée.
