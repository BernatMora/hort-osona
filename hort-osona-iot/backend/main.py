"""
main.py — Backend principal per a Hort Osona IoT

Rep dades dels sensors via MQTT, les desa a SQLite, i serveix una API REST
per a la PWA.

Temes MQTT:
  hort/sensors/miflora/<id>     → {moisture, light, temperature, fertility, conductivity}
  hort/sensors/thermometer/<id> → {temperature, humidity}
  hort/sensors/status           → {parcela, online, battery}

API REST:
  GET  /sensors                  → Llista totes les últimes lectures
  GET  /sensors/{parcela}        → Lectures d'una parcel·la
  GET  /sensors/{parcela}/history → Històric d'una parcel·la (últimes 24h)
  GET  /health                   → Estat del servei
"""

import json
import sqlite3
import time
from datetime import datetime, timedelta
from pathlib import Path

import paho.mqtt.client as mqtt
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# === Configuració ===
DB_PATH = Path("/opt/hort-osona-iot/data/sensors.db")
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC_PREFIX = "hort/sensors"

# === Base de dades ===
def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS lectures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            sensor_id TEXT NOT NULL,
            sensor_type TEXT NOT NULL,
            parcela TEXT,
            data_json TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE INDEX IF NOT EXISTS idx_sensor_ts
        ON lectures(sensor_id, ts)
    """)
    conn.commit()
    conn.close()
    print(f"[DB] Base de dades inicialitzada: {DB_PATH}")

# === MQTT ===
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[MQTT] Connectat al broker {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(f"{MQTT_TOPIC_PREFIX}/#")
        print(f"[MQTT] Subscrit a {MQTT_TOPIC_PREFIX}/#")
    else:
        print(f"[MQTT] Error de connexió: rc={rc}")

def on_message(client, userdata, msg):
    try:
        topic_parts = msg.topic.split("/")
        # hort/sensors/<tipus>/<id>
        if len(topic_parts) >= 4:
            sensor_type = topic_parts[2]
            sensor_id = topic_parts[3]
        else:
            sensor_type = "unknown"
            sensor_id = msg.topic

        data = json.loads(msg.payload.decode())
        parcela = data.get("parcela", sensor_id)
        ts = datetime.now().isoformat()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT INTO lectures (ts, sensor_id, sensor_type, parcela, data_json)
            VALUES (?, ?, ?, ?, ?)
        """, (ts, sensor_id, sensor_type, parcela, json.dumps(data)))
        conn.commit()
        conn.close()
        print(f"[MQTT] {sensor_type}/{sensor_id} → {data}")
    except Exception as e:
        print(f"[MQTT] Error processant missatge: {e}")

# === API REST ===
app = FastAPI(title="Hort Osona IoT API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permetre tots els orígens (PWA)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    return {
        "name": "Hort Osona IoT API",
        "version": "1.0.0",
        "endpoints": [
            "/health",
            "/sensors",
            "/sensors/{parcela}",
            "/sensors/{parcela}/history",
        ]
    }

@app.get("/health")
def health():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM lectures")
    total = c.fetchone()[0]
    c.execute("SELECT MAX(ts) FROM lectures")
    last_ts = c.fetchone()[0]
    conn.close()
    return {
        "status": "ok",
        "ts": datetime.now().isoformat(),
        "total_lectures": total,
        "last_reading": last_ts,
    }

@app.get("/sensors")
def list_sensors():
    """Retorna l'última lectura de cada sensor."""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT sensor_id, sensor_type, parcela, data_json, MAX(ts) as ts
        FROM lectures
        GROUP BY sensor_id
        ORDER BY ts DESC
    """)
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/sensors/{parcela}")
def get_parcela(parcela: str):
    """Retorna l'última lectura d'una parcel·la."""
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM lectures
        WHERE parcela = ?
        ORDER BY ts DESC
        LIMIT 1
    """, (parcela,))
    row = c.fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Parcel·la '{parcela}' no trobada")
    return dict(row)

@app.get("/sensors/{parcela}/history")
def get_history(parcela: str, hours: int = 24):
    """Retorna l'històric d'una parcel·la (per defecte últimes 24h)."""
    since = (datetime.now() - timedelta(hours=hours)).isoformat()
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT ts, data_json FROM lectures
        WHERE parcela = ? AND ts >= ?
        ORDER BY ts ASC
    """, (parcela, since))
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# === Main ===
if __name__ == "__main__":
    init_db()

    # Iniciar MQTT
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()

    # Iniciar API
    import uvicorn
    print("[API] Iniciant servidor FastAPI a 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
