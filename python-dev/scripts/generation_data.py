import random
from datetime import datetime, timedelta

# Nom du fichier
filename = "data.txt"

# Timestamp de début et fin 2024
start_date = datetime(2024, 1, 1, 0, 0)
end_date = datetime(2024, 12, 31, 23, 59)
delta_seconds = int((end_date - start_date).total_seconds())

# Liste des capteurs et types possibles
sensor_ids = [123, 124, 125]
types = {
    123: ["temperature", "humidity"],
    124: ["vibration"],
    125: ["temperature"]
}

# Génération de 1000 lignes
lines = []
for _ in range(1000):
    sensor_id = random.choice(sensor_ids)
    sensor_type = random.choice(types[sensor_id])
    
    # Valeurs plausibles
    if sensor_type == "temperature":
        value = round(random.uniform(20, 30), 1)
    elif sensor_type == "humidity":
        value = round(random.uniform(30, 60), 1)
    elif sensor_type == "vibration":
        value = round(random.uniform(0, 0.05), 3)
    
    # Timestamp aléatoire en secondes
    ts = int(start_date.timestamp()) + random.randint(0, delta_seconds)
    
    line = f"sensor_data,sensor_id={sensor_id},type={sensor_type} value={value} {ts}"
    lines.append(line)

# Écriture dans le fichier
with open(filename, "w") as f:
    f.write("\n".join(lines))

filename