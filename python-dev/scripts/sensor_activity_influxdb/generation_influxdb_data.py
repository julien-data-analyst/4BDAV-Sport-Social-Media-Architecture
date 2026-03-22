import random
import datetime
import psycopg2

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
            line = f"sensor_data,activity_id={act},user_sport_id={id_users_sports},sensor_metric={id_sensors_metrics}, value={valeur_quant} {ts}"
            lines.append(line)

    # Retourner le contenu
    return lines