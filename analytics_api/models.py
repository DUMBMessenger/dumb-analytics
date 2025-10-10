from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CpuInfo(BaseModel):
    name: Optional[str] = None
    cores: Optional[int] = None
    threads: Optional[int] = None
    freq: Optional[float] = None


class RamInfo(BaseModel):
    total: Optional[int] = None
    used: Optional[int] = None
    available: Optional[int] = None


class DiskEntry(BaseModel):
    mount: Optional[str] = None
    total: Optional[int] = None
    free: Optional[int] = None


class DisplayInfo(BaseModel):
    resolution: Optional[str] = None
    refresh_rate: Optional[int] = None
    dpi: Optional[int] = None
    monitor_count: Optional[int] = None


class BiosInfo(BaseModel):
    vendor: Optional[str] = None
    version: Optional[str] = None
    date: Optional[str] = None


class BaseTelemetry(BaseModel):
    type: str = Field(..., pattern=r"^(pc|android)$")
    device_id: str
    timestamp: Optional[float] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    kernel_version: Optional[str] = None
    hostname: Optional[str] = None
    uptime: Optional[float] = None
    timezone: Optional[str] = None
    locale: Optional[str] = None
    cpu: Optional[CpuInfo] = None
    ram: Optional[RamInfo] = None
    disks: Optional[List[DiskEntry]] = None
    display: Optional[DisplayInfo] = None
    gpu_name: Optional[str] = None
    gpu_vram: Optional[int] = None
    gpu_driver: Optional[str] = None
    bios: Optional[BiosInfo] = None
    motherboard_model: Optional[str] = None
    motherboard_vendor: Optional[str] = None


class AndroidTelemetry(BaseTelemetry):
    brand: Optional[str] = None
    manufacturer: Optional[str] = None
    android_version: Optional[str] = None
    sdk: Optional[int] = None
    battery_level: Optional[int] = None
    charging: Optional[bool] = None
    rooted: Optional[bool] = None
    storage: Optional[Dict[str, Any]] = None