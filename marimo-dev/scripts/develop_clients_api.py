import marimo

__generated_with = "0.20.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import psycopg2
    import redis
    from influxdb_client import InfluxDBClient
    from datetime import datetime, timezone

    return InfluxDBClient, datetime, psycopg2, redis, timezone


@app.cell
def _(InfluxDBClient, redis):
    r = redis.Redis(host="redis", decode_responses=True)
    influx_client = InfluxDBClient(url="http://influxdb_sensors_activity:8086", token="my-super-token", org="sports_org")
    query_api = influx_client.query_api()
    return query_api, r


@app.cell
def _(r):
    r
    return


@app.cell
def _():
    query = 'from(bucket:"sports_metrics")\
    |> range(start: -24h)\
    |> filter(fn:(r) => r.activity_id == "73")'
    return (query,)


@app.cell
def _(query, query_api):
    result = query_api.query(org="sports_org", query=query)
    return (result,)


@app.cell
def _(result):
    results = []
    for table in result:
      for record in table.records:
        results.append({
            "valeur" : record.get_value(), 
            "activity" : record.values.get("activity_id"),
            "sensor_metric" : record.values.get("sensor_metric"),
            "user_sport" : record.values.get("user_sport_id")
        })
    return (results,)


@app.cell
def _(results):
    print(results)
    return


@app.cell
def _(datetime, query_api, r, timezone):
    def get_finished_activities(influx_bucket, limit_activity):
        """Trouve les activités inactives depuis > 30 min dans InfluxDB"""
    
        query = f'''
        // On va récupérer la première et derière mesure pour chaque activité
        premieres_mesures = from(bucket: "{influx_bucket}")
          |> range(start: -24h)
          |> group(columns: ["activity_id", "sensor_metric", "user_sport_id"]) 
          |> first()
    
        dernieres_mesures = from(bucket: "{influx_bucket}")
          |> range(start: -24h)
          |> group(columns: ["activity_id", "sensor_metric", "user_sport_id"]) 
          |> last()'''+'\n join(tables: {p: premieres_mesures, d: dernieres_mesures}, on: ["activity_id", "sensor_metric", "user_sport_id"])'
    
        activity_data = {}
        now = datetime.now(timezone.utc)
        results = query_api.query(query)
    
        #print(results)
        for table in results:
        
                for record in table.records:
                    #print(record)
                    id = record.values.get("activity_id")
                    activity_data[id] = {
                    "sm" : record.values.get("sensor_metric"),
                    "us" : record.values.get("user_sport_id"),
                    "first_time" : record.values.get("_time_p"),
                    "last_time" : record.values.get("_time_d")
                    }

        # Filtrage par inactivité (30 min)
        finished = []
        for aid, times in activity_data.items():
            if times["last_time"]:
                diff_minutes = (now - times["last_time"]).total_seconds() / 60
                if diff_minutes > limit_activity:
                    if not r.sismember("processed_sessions", aid):
                        finished.append({
                            "id": aid,
                            "start_time": times["first_time"],
                            "end_time": times["last_time"],
                            "sm" : times["sm"],
                            "us" : times["us"]
                        })

        return finished

    return (get_finished_activities,)


@app.cell
def process_kpi_to_postgres(INFLUX_BUCKET, os, psycopg2, r):
    def process_kpi_to_postgres(session):
        """Calculer et insérer dans Postgres"""
        sid = session['id']
        print(f"--- Traitement session {sid} (Finie à {session['last_time']}) ---")

        # 1. Calcul (Exemple : somme d'une valeur sur toute la session)
        # On peut élargir le range ici pour être sûr de tout prendre
        q_sum = f'from(bucket:"{INFLUX_BUCKET}") |> range(start: -24h) |> filter(fn:(r) => r.session_id == "{sid}") |> sum()'
        # ... extraction de la valeur ...
        kpi_result = 123.45 

        # 2. Insertion Postgres
        try:
            with psycopg2.connect(os.getenv("POSTGRES_DSN")) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO kpis (session_id, total_value, closed_at) VALUES (%s, %s, NOW())",
                        (sid, kpi_result)
                    )

            # 3. Marquer comme traité dans Redis pour ne plus y revenir
            # On peut mettre un TTL de 24h sur cette info pour nettoyer Redis plus tard
            r.sadd("processed_sessions", sid)
            r.expire("processed_sessions", 86400) 
            print(f"Session {sid} enregistrée avec succès.")

        except Exception as e:
            print(f"Erreur Postgres : {e}")

    return


@app.cell
def _():
    # Config
    INFLUX_BUCKET = "sports_metrics"
    IDLE_LIMIT_MINUTES = 30
    return IDLE_LIMIT_MINUTES, INFLUX_BUCKET


@app.cell
def _(IDLE_LIMIT_MINUTES, INFLUX_BUCKET, get_finished_activities):
    get_finished_activities(INFLUX_BUCKET,IDLE_LIMIT_MINUTES)
    return


app._unparsable_cell(
    """
    def process_kpi_to_postgres(activities, influx_bucket):
        \"\"\"Calculer et insérer dans Postgres\"\"\"
        insertion_activity = []
    
        for activity in activities:
            sid = activity['id']
            start_iso = activity['start_time'].isoformat()
            end_iso = activity['end_time'].isoformat()
        
            print(f\"--- Traitement activité {sid} (Finie à {activity['end_time']}) ---\")
    
            # 1. Sélectionner les aggrégations à faire sur cette mesure
            liste_agg = []
            with psycopg2.connect(\"postgresql://postgres_social_media:5432?user=postgres&password=postgres\") as conn:
                 with conn.cursor() as cur:
                     cur.execute(f'''SELECT DISTINCT a.name, am.id FROM public.\"Aggregation\" AS a 
                     INNER JOIN public.\"Aggregation_Metric\" AS am ON am.id_aggregation = a.id 
                     INNER JOIN public.\"Sensors_Metrics\" AS sm ON sm.id_metric = am.id_metric 
                     WHERE sm.id='{activity['sm']}' '''
                                )
                     liste_agg = cur.fetchall()
    
            # 2. Insertion de l'activité finie dans la base 
            try:
                if not sid in insertion_activity: 
                 with psycopg2.connect(\"postgresql://postgres_social_media:5432?user=postgres&password=postgres\") as conn:
                     with conn.cursor() as cur:
                         cur.execute(f'''INSERT INTO public.\"Activity\" (id, beginning_date, ending_date, id_user_sport)
                         VALUES 
                         ('{sid}', '{activity[\"start_time\"]}', '{activity[\"end_time\"]}', '{activity[\"us\"]}')'''
                                    )
                insertion_activity.append(sid) # Ajout de l'activité insérée, cela permets d'éviter des duplications si on calcule plusieurs métriques pour cette activité
            
            except Exception as e:
                print(f\"Erreur requête d'insertion de l'activité : {e}\")

            # 3. Calcul des KPIs et insertion dans la base
            for kpi in liste_agg:
            
                query_kpi = f'from(bucket:\"{influx_bucket}\") |> range(start: {start_iso}, stop: {end_iso}) filter(fn:(r) => r.session_id == \"{sid}\") |> '
                if kpi[0] == \"min\":
                
                # Insertion postgres
                try:
                    with psycopg2.connect(\"postgresql://postgre_social_media:5432?user=postgres&password=postgres\") as conn:
                        with conn.cursor() as cur:
                            cur.execute(
                                \"INSERT INTO kpis (session_id, total_value, closed_at) VALUES (%s, %s, NOW())\",
                                (sid, kpi_result)
                            )
    
                # 3. Marquer comme traité dans Redis pour ne plus y revenir
                # On peut mettre un TTL de 24h sur cette info pour nettoyer Redis plus tard
                r.sadd(\"processed_sessions\", sid)
                r.expire(\"processed_sessions\", 86400) 
                print(f\"Session {sid} enregistrée avec succès.\")

            except Exception as e:
                print(f\"Erreur requête d'insertion des KPIs : {e}\")
    """,
    name="_"
)


@app.cell
def _(psycopg2):
    conn = psycopg2.connect("postgresql://postgres_social_media:5432?user=postgres&password=postgres")
    conn.cursor
    conn.close()
    return


@app.cell
def _():
    return


@app.cell
def _(query_api):
    query_2 = '''
    // On va récupérer la première et derière mesure pour chaque activité
    premieres_mesures = from(bucket: "sports_metrics")
      |> range(start: -24h)
      |> group(columns: ["activity_id", "sensor_metric", "user_sport_id"]) 
      |> first()

    dernieres_mesures = from(bucket: "sports_metrics")
      |> range(start: -24h)
      |> group(columns: ["activity_id", "sensor_metric", "user_sport_id"]) 
      |> last()

    join(tables: {p: premieres_mesures, d: dernieres_mesures}, on: ["activity_id", "sensor_metric", "user_sport_id"])
    '''

    activity_data_2 = []
    results_2 = query_api.query(query_2)

    print(results_2)
    for table_2 in results_2:
            #print(table_2)
    
            for record_2 in table_2.records:
                print(record_2)
                activity_data_2.append({
            "activity" : record_2.values.get("activity_id"),
            "sensor_metric" : record_2.values.get("sensor_metric"),
            "user_sport" : record_2.values.get("user_sport_id"),
            "first_time" : record_2.values.get("_time_p"),
            "last_time" : record_2.values.get("_time_d")
            })

    activity_data_2
    return


if __name__ == "__main__":
    app.run()
