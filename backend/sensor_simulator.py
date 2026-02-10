import random, time
from datetime import datetime
from database import get_connection

def insert_sensor_data(data):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO sensor_data (timestamp, temperature, humidity, pressure_diff, particle_count)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data["timestamp"], data["temperature"], data["humidity"],
        data["pressure_diff"], data["particle_count"]
    ))
    conn.commit()
    conn.close()

while True:
    data = {
        "timestamp": datetime.now().isoformat(),
        "temperature": round(random.uniform(17, 27), 2),
        "humidity": round(random.uniform(35, 65), 2),
        "pressure_diff": round(random.uniform(5, 20), 2),
        "particle_count": random.randint(200, 5000)
    }
    insert_sensor_data(data)
    print("Inserted:", data)
    time.sleep(3)
