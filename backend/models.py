from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AssetBase(BaseModel):
    name: str = Field(..., example="Smart Streetlight #01")
    category: str = Field(..., example="Lighting")
    latitude: float = Field(..., example=-3.7928)
    longitude: float = Field(..., example=102.2608)
    status: str = Field("Normal", example="Normal") # Normal, Warning, Critical, Offline

class AssetCreate(AssetBase):
    pass

class TelemetryData(BaseModel):
    asset_id: str
    temperature: float = Field(..., example=28.5)
    battery_level: float = Field(..., example=95.0)
    operational_status: str = Field("OK", example="OK")
    extra_sensors: Optional[Dict[str, Any]] = None

class Asset(AssetBase):
    id: str
    last_updated: datetime
    last_telemetry: Optional[TelemetryData] = None

class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: Dict[str, Any]
    properties: Dict[str, Any]

class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]
