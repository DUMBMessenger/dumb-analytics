import time
from typing import List, Dict, Any

from pydantic import BaseModel, Field

class BaseTelemetry(BaseModel):
    type: str = Field(..., pattern=r"^(pc|android|web)$")
    device_id: str
    timestamp: float = time.time()

class CpuInfo(BaseModel):
    name: str
    cores: int
    threads: int
    freq: float


class RamInfo(BaseModel):
    total: int
    used: int
    available: int


class DiskEntry(BaseModel):
    mount: str
    total: int
    free: int


class DisplayInfo(BaseModel):
    resolution: str
    refresh_rate: int
    dpi: int
    monitor_count: int


class BiosInfo(BaseModel):
    vendor: str
    version: str
    date: str


# PC telemetry
class PCTelemetry(BaseTelemetry):
    os_name: str
    os_version: str
    kernel_version: str
    hostname: str
    uptime: float
    timezone: str
    locale: str
    cpu: CpuInfo
    ram: RamInfo
    disks: List[DiskEntry]
    display: DisplayInfo
    gpu_name: str
    gpu_vram: int
    gpu_driver: str
    bios: BiosInfo
    motherboard_model: str
    motherboard_vendor: str

# Android telemetry
class AndroidTelemetry(BaseTelemetry):
    brand: str
    manufacturer: str
    android_version: str
    sdk: int
    battery_level: int
    charging: bool
    rooted: bool
    storage: Dict[str, Any]

# Web telemetry
class WebTelemetry(BaseTelemetry):
    user_agent: str
    platform: str
    language: str
    languages: List[str]
    vendor: str
    screen_width: int
    screen_height: int
    color_depth: int
    pixel_ratio: float
    timezone_offset: int
    performance_memory: Dict[str, Any]
    battery_level: float
    charging: bool
    storage_estimate: Dict[str, Any]
    connection: Dict[str, Any]
    hardware_concurrency: int
    device_memory: float
    touch_support: bool
    cookie_enabled: bool