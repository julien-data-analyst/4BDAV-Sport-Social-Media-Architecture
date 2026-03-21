import random
from faker import Faker

def generate_sql_script(nb_users=5, nb_sensors=5, nb_apparatus=5,sports=[
    ('1', 'Natation', 'Parmi les activités humaines, la natation regroupe le déplacement à la surface de l''eau et sous l''eau (plongée, mermaiding, natation synchronisée, water-polo), le plongeon et divers jeux pratiqués dans l''eau.'),
    ('2', 'Course à pieds (Trail)', 'Le trail, la course nature ou plus rarement la course en sentier, est un sport de course à pied, en milieu naturel, généralement sur des chemins de terre et des sentiers de randonnée en plaine, en forêt ou en montagne.')
    ], 
    metrics=[
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