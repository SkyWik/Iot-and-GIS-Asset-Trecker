# Tentang
Tugas Sesi 3 Internet of Things, Menggunakan Iot dan Gis
## Panduan Memulai
### Jalankan Backend API
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

### Buka Dashboard GIS Frontend
Buka file `frontend/index.html` langsung di browser web Anda, atau gunakan ekstensi *Live Server* di VS Code.

### Jalankan Simulator Sensor IoT
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
