from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import os
from typing import List, Dict
from models import Asset, AssetCreate, TelemetryData, GeoJSONFeature, GeoJSONFeatureCollection

app = FastAPI(
    title="GeoTrack-IoT API",
    description="Backend API untuk Sistem Manajemen Aset Geospasial & Telemetri IoT",
    version="1.0.0"
)

# Enable CORS for Web GIS Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-Memory Database (Loaded from seed data)
db_assets: Dict[str, dict] = {}

def load_seed_data():
    seed_path = os.path.join(os.path.dirname(__file__), "..", "data", "seed_assets.json")
    if os.path.exists(seed_path):
        with open(seed_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                item["last_updated"] = datetime.now()
                db_assets[item["id"]] = item
    else:
        # Fallback default seed
        default_items = [
            {
                "id": "AST-001",
                "name": "Lampu Jalan Pintar Pantai Panjang",
                "category": "Penerangan",
                "latitude": -3.8150,
                "longitude": 102.2780,
                "status": "Normal",
                "last_updated": datetime.now(),
                "last_telemetry": {
                    "asset_id": "AST-001",
                    "temperature": 29.2,
                    "battery_level": 88.0,
                    "operational_status": "OK",
                    "extra_sensors": {"lumens": 450, "motion_detected": False}
                }
            },
            {
                "id": "AST-002",
                "name": "Sensor Kualitas Air Sungai Muara",
                "category": "Lingkungan",
                "latitude": -3.7915,
                "longitude": 102.2612,
                "status": "Warning",
                "last_updated": datetime.now(),
                "last_telemetry": {
                    "asset_id": "AST-002",
                    "temperature": 32.1,
                    "battery_level": 45.0,
                    "operational_status": "Suhu Tinggi",
                    "extra_sensors": {"pH": 7.8, "turbidity_NTU": 14.2}
                }
            },
            {
                "id": "AST-003",
                "name": "TPS Pintar Simpang Lima",
                "category": "Kebersihan",
                "latitude": -3.7932,
                "longitude": 102.2655,
                "status": "Critical",
                "last_updated": datetime.now(),
                "last_telemetry": {
                    "asset_id": "AST-003",
                    "temperature": 35.0,
                    "battery_level": 15.0,
                    "operational_status": "Kapasitas Penuh & Baterai Lemah",
                    "extra_sensors": {"fill_level_percent": 95}
                }
            }
        ]
        for item in default_items:
            db_assets[item["id"]] = item

@app.on_event("startup")
def startup_event():
    load_seed_data()

@app.get("/", summary="Root Endpoint")
def read_root():
    return {
        "system": "GeoTrack-IoT Spatial Asset System",
        "status": "Operational",
        "total_assets": len(db_assets),
        "docs_url": "/docs"
    }

@app.get("/api/assets", response_model=List[dict], summary="Dapatkan Semua Aset")
def get_all_assets():
    return list(db_assets.values())

@app.get("/api/assets/{asset_id}", response_model=dict, summary="Dapatkan Detail Aset")
def get_asset(asset_id: str):
    if asset_id not in db_assets:
        raise HTTPException(status_code=404, detail="Aset tidak ditemukan")
    return db_assets[asset_id]

@app.post("/api/assets", status_code=status.HTTP_201_CREATED, summary="Tambah Aset Baru")
def create_asset(asset: AssetCreate):
    new_id = f"AST-{len(db_assets) + 1:03d}"
    new_asset = {
        "id": new_id,
        "name": asset.name,
        "category": asset.category,
        "latitude": asset.latitude,
        "longitude": asset.longitude,
        "status": asset.status,
        "last_updated": datetime.now(),
        "last_telemetry": None
    }
    db_assets[new_id] = new_asset
    return new_asset

@app.post("/api/telemetry", summary="Injest Telemetri IoT")
def receive_telemetry(telemetry: TelemetryData):
    asset_id = telemetry.asset_id
    if asset_id not in db_assets:
        raise HTTPException(status_code=404, detail=f"Aset ID {asset_id} tidak terdaftar")

    asset = db_assets[asset_id]
    asset["last_telemetry"] = telemetry.dict()
    asset["last_updated"] = datetime.now()

    # Logika Otomatisasi Status berdasarkan telemetri
    if telemetry.battery_level < 20 or telemetry.temperature > 40:
        asset["status"] = "Critical"
    elif telemetry.battery_level < 50 or telemetry.temperature > 32:
        asset["status"] = "Warning"
    else:
        asset["status"] = "Normal"

    return {
        "message": "Telemetri berhasil disimpan",
        "asset_id": asset_id,
        "updated_status": asset["status"]
    }

@app.get("/api/assets/geojson", summary="Export Data Aset ke Format Standard GeoJSON")
def get_assets_geojson():
    features = []
    for asset in db_assets.values():
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [asset["longitude"], asset["latitude"]]
            },
            "properties": {
                "id": asset["id"],
                "name": asset["name"],
                "category": asset["category"],
                "status": asset["status"],
                "telemetry": asset.get("last_telemetry")
            }
        }
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }
