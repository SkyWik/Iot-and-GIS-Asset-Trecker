# GeoTrack-IoT: Smart Spatial Asset & IoT Monitoring System

> **A Spatial IoT & GIS Asset Management System inspired by Spatial Data Analytics and Industrial Asset Management Case Studies.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Leaflet](https://img.shields.io/badge/GIS-Leaflet.js-orange.svg)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-teal.svg)

## 📌 Deskripsi Proyek (Project Overview)

**GeoTrack-IoT** adalah sistem pemantauan aset geospasial berbasis Internet of Things (IoT) dan Geographic Information System (GIS). Sistem ini dirancang untuk mengintegrasikan telemetri sensor IoT secara real-time dengan pemetaan spasial interaktif untuk manajemen aset publik/industri (seperti infrastruktur kota, penerangan jalan, fasilitas umum, dan sensor lingkungan).

Proyek ini dibuat berdasarkan studi kasus pemanfaatan GIS dan analisis geospasial dalam manajemen aset (misalnya di bidang properti, fasilitas, dan lingkungan).

---

## 🎯 Fitur Utama

- 📍 **Peta GIS Interaktif**: Visualisasi lokasi aset menggunakan Leaflet.js & OpenStreetMap.
- 📡 **Integrasi Sensor IoT**: Menerima & mengolah data telemetri real-time (suhu, baterai, status operasional, dll).
- 🗺️ **Format Standard GeoJSON**: API menyajikan data lokasi dalam standar spesifikasi OGC GeoJSON untuk kompatibilitas GIS (QGIS, ArcGIS Enterprise, FME).
- 🚨 **Peringatan Otomatis (Alerts)**: Deteksi otomatis status kritis (misal: suhu tinggi, baterai lemah, atau gangguan sinyal).
- 🧪 **Simulator Sensor IoT**: Script Python bawaan untuk menyimulasikan node sensor IoT yang mengirimkan data ke backend secara teratur.
- 📊 **Dashboard Ringkas**: Panel statistik ringkasan total aset, status aktif, peringatan, dan grafik telemetri.

---

## 🏗️ Arsitektur Sistem

```text
[ IoT Sensor Nodes / Simulator ] 
           │
           │ HTTP POST (Telemetry Data)
           ▼
┌────────────────────────────────────────┐
│      FastAPI Backend (REST API)        │
│   - Telemetry Ingestion                │
│   - GeoJSON Provider                   │
│   - Asset CRUD & Alert Engine          │
└───────────────────┬────────────────────┘
                    │
                    │ JSON / GeoJSON
                    ▼
┌────────────────────────────────────────┐
│      Web GIS Frontend (Leaflet.js)     │
│   - Interactive Map Layer              │
│   - Asset Marker & Popup               │
│   - Real-time Dashboard Panel          │
└────────────────────────────────────────┘
```

---

## 📁 Struktur Direktori

```text
iot-gis-asset-tracker/
├── backend/
│   ├── main.py            # Aplikasi FastAPI backend & endpoint REST/GeoJSON
│   ├── models.py          # Model data SQLAlchemy & Pydantic
│   └── requirements.txt    # Dependensi Python backend
├── frontend/
│   ├── index.html         # Halaman utama Web GIS Dashboard
│   ├── style.css          # Styling dashboard & peta interaktif
│   └── app.js             # Logika Leaflet.js & pemicu pembaruan real-time
├── simulator/
│   └── sensor_simulator.py # Simulator pengirim telemetri IoT
├── data/
│   └── seed_assets.json   # Data awal lokasi aset sampel (Kota Bengkulu / GIS Sample)
├── .gitignore             # File komitmen git yang dikecualikan
├── LICENSE                # Lisensi MIT
└── README.md              # Dokumentasi proyek
```

---

## 🚀 Panduan Memulai (Quick Start)

### 1. Prasyarat
- Python 3.9 atau versi yang lebih baru
- Browser web modern (Chrome, Firefox, Edge, Safari)

### 2. Jalankan Backend API
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
> Backend REST API & GeoJSON akan berjalan pada: `http://localhost:8000`  
> Dokumentasi API Swagger dapat diakses di: `http://localhost:8000/docs`

### 3. Buka Dashboard GIS Frontend
Buka file `frontend/index.html` langsung di browser web Anda, atau gunakan ekstensi *Live Server* di VS Code.

### 4. Jalankan Simulator Sensor IoT
Buka terminal baru untuk menyimulasikan pengiriman data telemetri dari perangkat sensor IoT ke backend:
```bash
cd simulator
python sensor_simulator.py
```

---

## 🛰️ Integrasi Perangkat Perangkat GIS (QGIS / ArcGIS)
Anda dapat menghubungkan endpoint GeoJSON dari sistem ini langsung ke software GIS seperti **QGIS** atau **ArcGIS Pro**:
- **GeoJSON Endpoint**: `http://localhost:8000/api/assets/geojson`
- Di QGIS: Pilih `Layer` -> `Add Layer` -> `Add Vector Layer` -> Masukkan URL HTTP di atas.

---

## 📄 Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT - lihat file [LICENSE](LICENSE) untuk detailnya.
