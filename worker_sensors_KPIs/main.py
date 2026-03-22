import os
import time
from datetime import datetime, timezone
import redis
import psycopg2
from influxdb_client import InfluxDBClient

# Config
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")
IDLE_LIMIT_MINUTES = 30

# Connexions
r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), decode_responses=True)
influx_client = InfluxDBClient(url=os.getenv("INFLUX_URL"), token=os.getenv("INFLUX_TOKEN"), org=os.getenv("INFLUX_ORG"))
query_api = influx_client.query_api()

def get_finished_sessions():
    """Trouve les sessions inactives depuis > 30 min dans InfluxDB"""
    # Flux : On cherche le dernier point de chaque session_id sur la dernière heure
    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "activity")
      |> group(columns: ["session_id"])
      |> last()
    '''
    
    finished = []
    now = datetime.now(timezone.utc)
    tables = query_api.query(query)

    for table in tables:
        for record in table.records:
            sid = record.values.get("session_id")
            last_time = record.get_time() # Objet datetime UTC
            
            # Calcul de l'écart
            diff_minutes = (now - last_time).total_seconds() / 60
            
            if diff_minutes > IDLE_LIMIT_MINUTES:
                # On vérifie dans Redis si on ne l'a pas déjà traitée
                if not r.sismember("processed_sessions", sid):
                    finished.append({"id": sid, "last_time": last_time})
    
    return finished

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

if __name__ == "__main__":
    print("Worker de détection d'inactivité démarré...")
    while True:
        try:
            sessions_to_process = get_finished_sessions()
            for s in sessions_to_process:
                process_kpi_to_postgres(s)
        except Exception as e:
            print(f"Erreur boucle : {e}")
            
        time.sleep(60) # Vérification toutes les minutes