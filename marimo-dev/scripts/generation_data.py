import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import random
    import datetime
    from faker import Faker
    import pandas as pd
    import psycopg2

    return Faker, datetime, mo, psycopg2, random


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Génération de données aléatoires**
    ## Auteur : Julien RENOULT
    ## Date : 19/03/2026
    ### *Promo : PGE.4 Spécialité Data*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introduction
    Ici, vous trouverez ci-joint le travail mené pour générer aléatoirement les données fictives afin de tester nos bases de données et la consistence de celle-ci. On commencera d'abord par les données SQL à gérer qui seront insérées avec un script SQL généré. Ensuite on aura influxDB avec la génération d'un TXT se basant sur les données de notre base SQL. Pour finir, on générera les données pour le réseau social avec Redis en générant un schéma typique de JSON.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Génération de données aléatoires pour SQL

    Ici, nous allons générer le script SQL pour insérer les données aléatoires qui seront utilisées dans la liste des options proposées, vous pourrez modifier celle-ci afin de tester d'autre types de données et voir les cas d'usages.
    """)
    return


@app.cell
def _(Faker, random):
    def generate_sql_script(nb_users=5, nb_sensors=5, nb_apparatus=5,sports=[
        ('1', 'Natation', 'Parmi les activités humaines, la natation regroupe le déplacement à la surface de l''eau et sous l''eau (plongée, mermaiding, natation synchronisée, water-polo), le plongeon et divers jeux pratiqués dans l''eau.'),

    ('2', 'Course à pieds (Trail)', 'Le trail, la course nature ou plus rarement la course en sentier, est un sport de course à pied, en milieu naturel, généralement sur des chemins de terre et des sentiers de randonnée en plaine, en forêt ou en montagne.')
    ], metrics=[
            ("1", "Distance parcourue (km) ", "km"),
            ("2", "Vitesse (km/h) ", "km/h"),
            ("3", "Nombre de mouvements de nages", None),
            ("4", "SWOLF", None),
        ],
                           sports_metrics = [
                               ("1", "1", "3"),
                               ("2", "1", "4"),
                               ("3", "2", "1"),
                               ("4", "2", "2")
                           ]):
        """
        Génère un script SQL d'insertion PostgreSQL avec des données aléatoires cohérentes.
        :param nb_users: nombre d'utilisateurs à générer
        :param nb_sensors: nombre de capteurs à générer
        :param sports: liste de tuple représentant les sports à insérer (id, name, description)
        :param metrics : liste de tuple représentant les métrique à insérer (id, name, unity)
        :param sports_metrics : liste de tuple représentant la liaison entre les sports et leurs métriques
        :return: string contenant le script SQL complet
        """

        fake = Faker("fr_FR")
        sql = []

        # -----------------------------
        # USERS (génération via Faker de profils d'utilisateurs)
        # -----------------------------

        # génération d'utilisateurs
        print("---- Génération d'utilisateurs ----")
        users = []
        for i in range(1, nb_users + 1):
            users.append({
                "id": i,
                "firstname": fake.first_name(),
                "lastname": fake.last_name(),
                "description": fake.text(max_nb_chars=80).replace("'", ""),
                "email": fake.email(),
                "password": fake.password(length=8).replace("'", "")
            })

        # Insertion dans le script SQL
        sql.append('INSERT INTO "User" (id, firstname, lastname, description, email, password) VALUES')
        sql.append(",\n".join([
            f"('{u['id']}', '{u['firstname']}', '{u['lastname']}', '{u['description']}','{u['email']}', '{u['password']}')"
            for u in users
        ]) + ";\n")

        # -----------------------------
        # SPORTS (insertion de la liste de tuple directement dans le texte)
        # -----------------------------
        print("---- Génération de sports ----")
        # Insertion dans le script SQL
        sql.append('INSERT INTO "Sport" (id, name, description) VALUES')
        sql.append(",\n".join([f"('{s[0]}', '{s[1]}', '{s[2]}')"
            for s in sports
        ]) + ";\n")

        # -----------------------------
        # METRICS (insertion de la liste de tuple directement dans le texte)
        # -----------------------------
        print("---- Génération de métriques ----")
        sql.append('INSERT INTO "Metric" (id, name, unity) VALUES')
        sql.append(",\n".join([
            f"('{m[0]}', '{m[1]}', { 'NULL' if m[2] is None else "'" + m[2] + "'" })"
            for m in metrics
        ]) + ";\n")

        # -----------------------------
        # SPORTS_METRICS (insertion de la liste de tuple directement dans le texte)
        # -----------------------------
        print("---- Génération des relations entre le sport et les métriques associées ----")
        sql.append('INSERT INTO "Sports_Metrics" (id, sport_id, metric_id) VALUES')
        sql.append(",\n".join([
            f"('{ms[0]}', '{ms[1]}', '{ms[2]}')"
            for ms in sports_metrics
        ]) + ";\n")

        # -----------------------------
        # USER_SPORTS (relations FK)
        # -----------------------------
        print("---- Génération des sports réalisés par les utilisateurs ----")
        user_sports = []
        us_id = 1 # l'id de us_sports

        for user in users:
            # chaque user a 1 à 2 sports
            for sport in random.sample(sports, k=random.randint(1, min(2, len(sports)))):
                user_sports.append((str(us_id), user["id"], sport[0]))
                us_id += 1

        # Insertion dans le script SQL
        sql.append('INSERT INTO "User_Sports" (id, user_id, sport_id) VALUES')
        sql.append(",\n".join([
            f"('{us[0]}', '{us[1]}', '{us[2]}')"
            for us in user_sports
        ]) + ";\n")

        # -----------------------------
        # PROFESSIONNAL (subset de User_Sports)
        # -----------------------------
        print("---- Génération des professionnel sportifs ----")
        pros = []
        for i, us in enumerate(random.sample(user_sports, k=max(1, len(user_sports)//2)), start=1):
            pros.append((i, us[0], fake.job().replace("'", ""), fake.text(max_nb_chars=60).replace("'", "")))

        sql.append('INSERT INTO "Professionnal" (id, user_sport_id, title, description) VALUES')
        sql.append(",\n".join([
            f"('{p[0]}', '{p[1]}', '{p[2]}', '{p[3]}')"
            for p in pros
        ]) + ";\n")

        # -----------------------------
        # SENSOR
        # -----------------------------
        print("---- Génération de capteurs ----")
        sensors = []
        for id_sens in range(1, nb_sensors+1):
            sensors.append((id_sens, fake.word().replace("'", ""), 
                            random.choice(["montre", "bracelet", "capteur"]), None, None))

        sql.append('INSERT INTO "Sensor" (id, name, type, formula) VALUES')
        sql.append(",\n".join([
            f"('{s[0]}', '{s[1]}', '{s[2]}', NULL)"
            for s in sensors
        ]) + ";\n")

        # -----------------------------
        # APPARATUS
        # -----------------------------
        print("---- Génération d'appareils ----")
        apparatus = []
        for id_app in range(1, nb_apparatus+1):
            apparatus.append((id_app, fake.word().replace("'", ""), random.choice(["mobile", "montre", "tablette"])))

        sql.append('INSERT INTO "Apparatus" (id, name, type) VALUES')
        sql.append(",\n".join([
            f"('{a[0]}', '{a[1]}', '{a[2]}')"
            for a in apparatus
        ]) + ";\n")

        # -----------------------------
        # SENSORS_APPARATUS (relations)
        # -----------------------------
        print("---- Génération des liaisons entre l'appareil et le capteur ----")
        sensors_apparatus = []
        sa_id = 1
        # Un capteur doit avoir forcément un appareil au moins de reliés
        for sen in sensors:
            # échantillonage sur la liste des appareils afin de récupérer leur id
            for app in random.sample(apparatus, k=random.randint(1, len(apparatus))):
                sensors_apparatus.append((sa_id, sen[0], app[0]))
                sa_id += 1

        sql.append('INSERT INTO "Sensors_Apparatus" (id, sensor_id, apparatus_id) VALUES')
        sql.append(",\n".join([
            f"('{sens_apps[0]}', '{sens_apps[1]}', '{sens_apps[2]}')"
            for sens_apps in sensors_apparatus
        ]) + ";\n")

        # -----------------------------
        # AGGREGATION (données fixes car ce sont des méthodes de calculs pour les KPIs)
        # -----------------------------
        print("---- Génération des aggrégations ----")
        liste_aggregation = [('1', 'min'),
        ('2', 'max'),
        ('3', 'mean'),
        ('4', 'median'),
        ('5', 'Q1'),
        ('6', 'Q3'),
        ('7', 'standard deviation'),
        ('8', 'variability')]

        sql.append('INSERT INTO "Aggregation" (id, name) VALUES ')
        sql.append(",\n".join([
            f"('{agg[0]}', '{agg[1]}')"
            for agg in liste_aggregation
        ]) + ";\n")

        # -----------------------------
        # AGGREGATION_METRIC (relation entre AGGREGATION et METRIC)
        # -----------------------------
        print("---- Génération des liaisons entre les aggrégations et métriques ----")
        agg_metric = []
        id_agg_metric = 0
        for metric in metrics: # Parcourir toutes les métriques

            for agg in liste_aggregation: # Pour des raisons de simplicité, nous ajoutons toutes les aggrégations par défaut
                agg_metric.append((id_agg_metric, f"{metric[1]} agg {agg[1]}", metric[0], agg[0]))
                id_agg_metric +=1

        # Insertion dans le script SQL
        sql.append('INSERT INTO "Aggregation_Metric" (id, name, id_metric, id_aggregation) VALUES')
        sql.append(",\n".join([
            f"('{am[0]}', '{am[1]}', '{am[2]}', '{am[3]}')"
            for am in agg_metric
        ]) + ";\n")

        # ----------------------------
        # SENSORS_METRICS (relation entre SENSOR et METRIC)
        # ----------------------------
        print("---- Génération des liaisons entre les capteurs et métriques ----")
        sensors_metrics = []
        sm_id = 1

        # Gérer le nombre de type de mesure que peut avoir un capteur
        if len(metrics) <=3 :
            nb_elt = len(metrics)
        else:
            nb_elt = 3

        # Un capteur doit avoir forcément une mesure type qui peut mesurer
        for sen in sensors:
            # échantillonage sur la liste des métriques afin de récupérer leur id
            for metr in random.sample(metrics, k=random.randint(1, nb_elt)):
                sensors_metrics.append((sm_id, sen[0], metr[0]))
                sm_id += 1

        sql.append('INSERT INTO "Sensors_Metrics" (id, id_sensor, id_metric) VALUES')
        sql.append(",\n".join([
            f"('{sens_metr[0]}', '{sens_metr[1]}', '{sens_metr[2]}')"
            for sens_metr in sensors_metrics
        ]) + ";\n")

        # ------------------------------
        # -----------------------------
        # RETURN FINAL SQL
        # -----------------------------
        return "\n".join(sql)

    return (generate_sql_script,)


@app.cell
def _(generate_sql_script):
    script = generate_sql_script()
    print(script)
    return


@app.cell
def _(generate_sql_script):
    with open("./scripts/data/dummy_data.sql", "w", encoding="utf-8") as f:
        f.write(generate_sql_script(nb_users=1000, nb_sensors=1000, nb_apparatus=500))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Génération de données aléatoires pour InfluxDB
    Ici, nous allons générer un fichier TXT pour insérer les données d'activité générée par des capteurs.

    schéma : sensor_data activity_id, user_sport_id, sensor_id, metric_id, value
    """)
    return


@app.cell
def _(psycopg2):
    # Récupérer les ids des différentes tables afin de générer les données fictives pour les activités des capteurs
    #Define our connection string
    conn_string = "host='postgres' port='5432' dbname='social_media_sports' user='postgres' password='postgres'"

    # print the connection string we will use to connect
    print("Connecting to database ->", conn_string)
    try:
        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(host="postgres",  
            port=5432,
            dbname="social_media_sports",
            user="postgres",
            password="postgres")

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        print("Connected!")
    except Exception as e:
        print(e)
    return conn, cursor


@app.cell
def _(conn, cursor):
    try:
        # Votre code précédent qui a probablement échoué
        cursor.execute('SELECT DISTINCT us.id, smetr.id FROM public."User_Sports" AS us INNER JOIN public."Sport" AS s ON s.id = us.sport_id INNER JOIN public."Sports_Metrics" AS sm ON sm.sport_id = s.id INNER JOIN public."Sensors_Metrics" AS smetr ON sm.metric_id = smetr.id_metric;')
    except Exception as e:
        print(f"Erreur détectée : {e}")
        conn.rollback()  # <--- Crucial : remet la transaction à zéro
    return


@app.cell
def _(cursor):
    id_users_sports_sensors_metrics = cursor.fetchall()
    return (id_users_sports_sensors_metrics,)


@app.cell
def _(id_users_sports_sensors_metrics):
    len(id_users_sports_sensors_metrics)
    return


@app.cell
def _(id_users_sports_sensors_metrics):
    id_users_sports_sensors_metrics[:5]
    return


@app.cell
def _(conn):
    conn.close()
    return


@app.cell
def _():
    filename = "scripts/data/sensors_activities_data.txt"
    lines = []
    return filename, lines


@app.cell
def _(datetime, filename, id_users_sports_sensors_metrics, lines, random):
    for act in range (1, 101):
        ###############
        # Première étape : choisir aléatoirement dans la liste "id_users_sports_sensors_metrics" les ids pour l'activité
        ###############
        choix_ussm = random.choice(id_users_sports_sensors_metrics)
        id_users_sports = choix_ussm[0] # Récupération des ids concernés
        id_sensors_metrics = choix_ussm[1]

        ############
        # Deuxième étape : choisir aléatoirement la journée dans l'année 2026 et aléatoirement le début et la fin qu'on va s'en servir pour déterminer aléatoirement les points de captures
        ############
         # Choisir un jour aléatoire en 2026
        debut_annee = datetime.date(2026, 1, 1)
        # Nombre de jours en 2026
        jour_aleatoire = debut_annee + datetime.timedelta(days=random.randint(0, 364))

        # 2. Définir une heure de début (ex: entre 06:00 et 20:00)
        heure_debut = random.randint(6, 20)
        minute_debut = random.randint(0, 59)

        debut_capture = datetime.datetime.combine(
            jour_aleatoire, 
            datetime.datetime.min.time().replace(hour=heure_debut, minute=minute_debut)
        )

        # 3. Définir une durée de session (ex: entre 15 minutes et 3 heures)
        duree_minutes = random.randint(15, 180)
        fin_capture = debut_capture + datetime.timedelta(minutes=duree_minutes)

        delta_seconds = int((fin_capture - debut_capture).total_seconds())
        ############
        # Troisième étape : génération d'une centaine de mesures pour une activité
        ############
        for mes in range(100):

            # 1. Générer une valeur quantitative aléatoire (float)
            valeur_quant = round(random.uniform(1, 30), 3)

            # 2. générer la date et l'heure de capture entre les deux datetime (début_capture, fin_capture)
            ts = int(debut_capture.timestamp()) + random.randint(0, delta_seconds)

            # 3. Création de la ligne de données + ajout dans le fichier TXT
            line = f"sensor_data,activity_id={act},user_sport_id={id_users_sports},sensor_metric={id_sensors_metrics}, value={valeur_quant} {ts}"
            lines.append(line)

    # Écriture dans le fichier
    with open(filename, "w") as influxdb_data:
        influxdb_data.write("\n".join(lines))        
    return


@app.cell
def _(datetime, psycopg2, random):
    def generation_influxdb_data(nb_act=100, nb_mesures=100, max_duree_session_minutes=180 ):
        """
        Génère un fichier de données TXT pour la base de données influxdb afin de simuler des données d'activités
        :return: string contenant le script SQL complet
        """
        lines=[]

        try:
            # Essayer de se connecter à la base de données
            conn = psycopg2.connect(host="postgres",  
                port=5432,
                dbname="social_media_sports",
                user="postgres",
                password="postgres")

            # Récupérer le curseur pour les requêtes
            cursor = conn.cursor()
            #print("Connected!")
        except Exception as e:
            raise ConnectionError(f"Erreur de connexion dans la bdd postgresql : {e}")
    
        try:
            # Récupérer les ids afin de les utiliser pour la génération de données
            cursor.execute('''SELECT DISTINCT us.id, smetr.id FROM public."User_Sports" AS us 
            INNER JOIN public."Sport" AS s ON s.id = us.sport_id 
            INNER JOIN public."Sports_Metrics" AS sm ON sm.sport_id = s.id 
            INNER JOIN public."Sensors_Metrics" AS smetr ON sm.metric_id = smetr.id_metric;''')

        except Exception as e:
            conn.rollback()
            raise ValueError(f" Erreur au niveau de la requête : {e}")
        
        id_users_sports_sensors_metrics = cursor.fetchall()
        conn.close()


        for act in range (1, nb_act+1):
            ###############
            # Première étape : choisir aléatoirement dans la liste "id_users_sports_sensors_metrics" les ids pour l'activité
            ###############
            choix_ussm = random.choice(id_users_sports_sensors_metrics)
            id_users_sports = choix_ussm[0] # Récupération des ids concernés
            id_sensors_metrics = choix_ussm[1]

            ############
            # Deuxième étape : choisir aléatoirement le début/fin de l'activité à partir de la date d'aujourd'hui. 
            ############
             # récupérer la date d'aujourd'hui
            debut_capture = datetime.date.today()

            # 2. Définir une heure de début (ex: entre 06:00 et 18:00)
            heure_debut = random.randint(6, 18)
            minute_debut = random.randint(0, 59)

            debut_capture = datetime.datetime.combine(
                debut_capture, 
                datetime.datetime.min.time().replace(hour=heure_debut, minute=minute_debut)
            )

            # 3. Définir une durée de session (ex: entre 15 minutes et 3 heures)
            duree_minutes = random.randint(15, max_duree_session_minutes)
            fin_capture = debut_capture + datetime.timedelta(minutes=duree_minutes)

            delta_seconds = int((fin_capture - debut_capture).total_seconds())

            ############
            # Troisième étape : génération des mesures pour l'activité concernée
            ############
            for mes in range(nb_mesures):

                # 1. Générer une valeur quantitative aléatoire (float)
                valeur_quant = round(random.uniform(1, 30), 3)

                # 2. générer la date et l'heure de capture entre les deux datetime (début_capture, fin_capture)
                ts = int(debut_capture.timestamp()) + random.randint(0, delta_seconds)

                # 3. Création de la ligne de données + ajout dans le fichier TXT
                line = f"sensor_data,activity_id={act},user_sport_id={id_users_sports},sensor_metric={id_sensors_metrics} value={valeur_quant} {ts}"
                lines.append(line)

        # Retourner le contenu
        return lines

    return (generation_influxdb_data,)


@app.cell
def _(filename, generation_influxdb_data):
    lines_influxdb = generation_influxdb_data()
    # Écriture dans le fichier
    with open(filename, "w") as influx:
        influx.truncate(0)
        influx.write("\n".join(lines_influxdb)) 
    return


if __name__ == "__main__":
    app.run()
