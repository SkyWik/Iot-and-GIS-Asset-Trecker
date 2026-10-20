import time
import random
import json
import urllib.request
import urllib.error

API_URL = "http://localhost:8000/api/telemetry"

# List Node Sensor IoT untuk disimulasikan
SENSORS = [
    {"asset_id": "AST-001", "temp_base": 28.0, "bat_base": 90.0},
    {"asset_id": "AST-002", "temp_base": 31.0, "bat_base": 48.0},
    {"asset_id": "AST-003", "temp_base": 34.0, "bat_base": 18.0},
    {"asset_id": "AST-004", "temp_base": 26.5, "bat_base": 98.0},
    {"asset_id": "AST-005", "temp_base": 27.2, "bat_base": 85.0},
]

print("🚀 Menseimulasikan Pengiriman Telemetri Sensor IoT ke Backend GIS...")
print("Tekan Ctrl+C untuk menghentikan simulator.\n")

try:
    while True:
        for s in SENSORS:
            # Variasikan suhu dan level baterai secara acak
            temp = round(s["temp_base"] + random.uniform(-1.5, 2.5), 1)
            battery = max(0.0, round(s["bat_base"] - random.uniform(0.0, 0.5), 1))
            s["bat_base"] = battery # Simulasikan konsumsi baterai perlahan

            payload = {
                "asset_id": s["asset_id"],
                "temperature": temp,
                "battery_level": battery,
                "operational_status": "OK" if battery > 20 and temp < 38 else "Peringatan Sistem",
                "extra_sensors": {
                    "signal_rssi_dbm": random.randint(-85, -50),
                    "uptime_hours": random.randint(100, 500)
                }
            }

            req = urllib.request.Request(
                API_URL,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )

            try:
                with urllib.request.urlopen(req) as response:
                    res_body = json.loads(response.read().decode('utf-8'))
                    print(f"✅ [{s['asset_id']}] Telemetri Terkirim | Temp: {temp}°C | Battery: {battery}% | Status: {res_body.get('updated_status')}")
            except urllib.error.URLError as e:
                print(f"❌ [{s['asset_id']}] Gagal terhubung ke API ({API_URL}): {e}")

        time.sleep(4)
except KeyboardInterrupt:
    print("\n🛑 Simulator dihentikan oleh pengguna.")
