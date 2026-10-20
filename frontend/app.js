// Base API Configuration
const API_URL = 'http://localhost:8000/api';

// Initialize Leaflet Map centered at Bengkulu City Center
const map = L.map('map').setView([-3.7928, 102.2608], 13);

// Add OpenStreetMap Dark Tile Layer
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
}).addTo(map);

// Global Markers Store
let markersMap = {};
let currentAssets = [];

// Icon Color Helper
function getMarkerColor(status) {
    switch (status) {
        case 'Normal': return '#4ade80';
        case 'Warning': return '#facc15';
        case 'Critical': return '#f87171';
        default: return '#38bdf8';
    }
}

// Create Custom Circle Marker
function createCustomMarker(asset) {
    const color = getMarkerColor(asset.status);
    const marker = L.circleMarker([asset.latitude, asset.longitude], {
        radius: 10,
        fillColor: color,
        color: '#ffffff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.85
    });

    const popupContent = `
        <div style="color: #0f172a; font-family: Inter, sans-serif;">
            <h4 style="margin: 0 0 4px 0; font-size: 14px;">${asset.name}</h4>
            <p style="margin: 0 0 6px 0; font-size: 11px; color: #64748b;">ID: ${asset.id} | ${asset.category}</p>
            <div style="font-size: 12px; margin-bottom: 6px;">
                Status: <strong style="color: ${color};">${asset.status}</strong>
            </div>
            <button onclick="selectAsset('${asset.id}')" style="background: #0284c7; color: white; border: none; padding: 4px 8px; border-radius: 4px; cursor: pointer; font-size: 11px;">Lihat Telemetri</button>
        </div>
    `;

    marker.bindPopup(popupContent);
    return marker;
}

// Fetch Assets from API
async function fetchAssets() {
    try {
        const response = await fetch(`${API_URL}/assets`);
        if (!response.ok) throw new Error('Gagal mengambil data dari API');
        const assets = await response.json();
        currentAssets = assets;
        
        updateMapAndUI(assets);
        document.getElementById('last-updated-text').textContent = `Terakhir diperbarui: ${new Date().toLocaleTimeString('id-ID')}`;
    } catch (err) {
        console.warn('API Offline atau tidak terjangkau, menggunakan data contoh...', err);
        // Fallback UI notification
        document.getElementById('last-updated-text').textContent = `Status API: Offline (Memuat sampel lokal)`;
    }
}

// Update Map & Sidebar UI
function updateMapAndUI(assets) {
    // Clear old markers
    Object.values(markersMap).forEach(m => map.removeLayer(m));
    markersMap = {};

    let counts = { Normal: 0, Warning: 0, Critical: 0 };
    const listContainer = document.getElementById('asset-list');
    listContainer.innerHTML = '';

    assets.forEach(asset => {
        // Count statuses
        if (counts[asset.status] !== undefined) counts[asset.status]++;

        // Add Marker
        const marker = createCustomMarker(asset);
        marker.addTo(map);
        markersMap[asset.id] = marker;

        // Add Card in Sidebar
        const card = document.createElement('div');
        card.className = 'asset-card';
        card.onclick = () => selectAsset(asset.id);
        card.innerHTML = `
            <div class="asset-header">
                <span class="asset-name">${asset.name}</span>
                <span class="status-badge status-${asset.status}">${asset.status}</span>
            </div>
            <div class="asset-sub">ID: ${asset.id} | Lat: ${asset.latitude.toFixed(4)}, Lon: ${asset.longitude.toFixed(4)}</div>
        `;
        listContainer.appendChild(card);
    });

    // Update Counter Badges
    document.getElementById('total-assets-count').textContent = assets.length;
    document.getElementById('normal-count').textContent = counts.Normal;
    document.getElementById('warning-count').textContent = counts.Warning;
    document.getElementById('critical-count').textContent = counts.Critical;
}

// Select Asset & Focus
window.selectAsset = function(assetId) {
    const asset = currentAssets.find(a => a.id === assetId);
    if (!asset) return;

    // Pan map to asset
    map.flyTo([asset.latitude, asset.longitude], 15, { duration: 1.2 });
    
    if (markersMap[assetId]) {
        markersMap[assetId].openPopup();
    }

    // Render Telemetry Detail
    const detailPanel = document.getElementById('detail-panel');
    detailPanel.classList.remove('hidden');

    const telemetry = asset.last_telemetry || {};
    const extra = telemetry.extra_sensors || {};

    let extraRows = '';
    for (const [key, val] of Object.entries(extra)) {
        extraRows += `
            <div class="detail-row">
                <span class="detail-label">${key}</span>
                <span class="detail-val">${val}</span>
            </div>
        `;
    }

    document.getElementById('detail-content').innerHTML = `
        <div class="detail-row">
            <span class="detail-label">Nama Aset</span>
            <span class="detail-val">${asset.name}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Kategori</span>
            <span class="detail-val">${asset.category}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Suhu Node</span>
            <span class="detail-val">${telemetry.temperature ? telemetry.temperature + ' °C' : 'N/A'}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Level Baterai</span>
            <span class="detail-val">${telemetry.battery_level ? telemetry.battery_level + ' %' : 'N/A'}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Status Operasional</span>
            <span class="detail-val">${telemetry.operational_status || 'OK'}</span>
        </div>
        ${extraRows}
    `;
};

// Refresh button event listener
document.getElementById('refresh-btn').addEventListener('click', fetchAssets);

// Initial Load & Auto Poll every 5 seconds
fetchAssets();
setInterval(fetchAssets, 5000);
