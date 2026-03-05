from pydantic import BaseModel
from typing import List, Optional

class EDAInfo(BaseModel):
    tool: str
    version: str
    path: str
    features: List[str]
    license_ok: bool

class DeviceLibrary(BaseModel):
    vivado: List[Dict]
    quartus: List[Dict]
    yosys: List[Dict]

class HardwareInventory(BaseModel):
    vendor_id: str
    product_id: str
    type: str
    interface: str
    confirmed_alive: bool

class ModelFile(BaseModel):
    path: str
    name: str
    type: str
    sha256: str

class FPGASystemProfile(BaseModel):
    eda_toolchain: List[EDAInfo]
    device_libraries: DeviceLibrary
    hardware_inventory: List[HardwareInventory]
    model_files: List[ModelFile]
    consecutive_passes: int = 0
    memory_hit_rate: float = 0.0