from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class CpuInfo(BaseModel):
    name: Optional[str] = "anonymized"
    cores: Optional[int] = "anonymized"
    threads: Optional[int] = "anonymized"
    freq: Optional[float] = "anonymized"


class RamInfo(BaseModel):
    total: Optional[int] = "anonymized"
    used: Optional[int] = "anonymized"
    available: Optional[int] = "anonymized"


class DiskEntry(BaseModel):
    mount: Optional[str] = "anonymized"
    total: Optional[int] = "anonymized"
    free: Optional[int] = "anonymized"


class DisplayInfo(BaseModel):
    resolution: Optional[str] = "anonymized"
    refresh_rate: Optional[int] = "anonymized"
    dpi: Optional[int] = "anonymized"
    monitor_count: Optional[int] = "anonymized"


class BiosInfo(BaseModel):
    vendor: Optional[str] = "anonymized"
    version: Optional[str] = "anonymized"
    date: Optional[str] = "anonymized"


class BaseTelemetry(BaseModel):
    type: str = Field(..., pattern=r"^(pc|android|web)$")
    device_id: str
    timestamp: Optional[float] = "anonymized"
    os_name: Optional[str] = "anonymized"
    os_version: Optional[str] = "anonymized"
    kernel_version: Optional[str] = "anonymized"
    hostname: Optional[str] = "anonymized"
    uptime: Optional[float] = "anonymized"
    timezone: Optional[str] = "anonymized"
    locale: Optional[str] = "anonymized"
    cpu: Optional[CpuInfo] = "anonymized"
    ram: Optional[RamInfo] = "anonymized"
    disks: Optional[List[DiskEntry]] = "anonymized"
    display: Optional[DisplayInfo] = "anonymized"
    gpu_name: Optional[str] = "anonymized"
    gpu_vram: Optional[int] = "anonymized"
    gpu_driver: Optional[str] = "anonymized"
    bios: Optional[BiosInfo] = "anonymized"
    motherboard_model: Optional[str] = "anonymized"
    motherboard_vendor: Optional[str] = "anonymized"


class AndroidTelemetry(BaseTelemetry):
    brand: Optional[str] = "anonymized"
    manufacturer: Optional[str] = "anonymized"
    android_version: Optional[str] = "anonymized"
    sdk: Optional[int] = "anonymized"
    battery_level: Optional[int] = "anonymized"
    charging: Optional[bool] = "anonymized"
    rooted: Optional[bool] = "anonymized"
    storage: Optional[Dict[str, Any]] = "anonymized"

class WebTelemetry(BaseTelemetry):
    user_agent: Optional[str] = "anonymized"
    platform: Optional[str] = "anonymized"
    language: Optional[str] = "anonymized"
    languages: Optional[list[str]] = "anonymized"
    vendor: Optional[str] = "anonymized"
    screen_width: Optional[int] = "anonymized"
    screen_height: Optional[int] = "anonymized"
    color_depth: Optional[int] = "anonymized"
    pixel_ratio: Optional[float] = "anonymized"
    timezone_offset: Optional[int] = "anonymized"
    performance_memory: Optional[Dict[str, Any]] = "anonymized"
    battery_level: Optional[float] = "anonymized"
    charging: Optional[bool] = "anonymized"
    storage_estimate: Optional[Dict[str, Any]] = "anonymized"
    connection: Optional[Dict[str, Any]] = "anonymized"
    hardware_concurrency: Optional[int] = "anonymized"
    device_memory: Optional[float] = "anonymized"
    touch_support: Optional[bool] = "anonymized"
    cookie_enabled: Optional[bool] = "anonymized"