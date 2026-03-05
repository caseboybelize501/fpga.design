import json
import os
from typing import List, Dict
from pydantic import BaseModel

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

# System Profile
class FPGASystemProfile(BaseModel):
    eda_toolchain: List[EDAInfo]
    device_libraries: DeviceLibrary
    hardware_inventory: List[HardwareInventory]
    model_files: List[ModelFile]
    consecutive_passes: int = 0
    memory_hit_rate: float = 0.0
    
    @classmethod
    def load(cls):
        try:
            with open("system_profile.json", "r") as f:
                data = json.load(f)
                return cls(**data)
        except FileNotFoundError:
            return cls(
                eda_toolchain=[],
                device_libraries=DeviceLibrary(vivado=[], quartus=[], yosys=[]),
                hardware_inventory=[],
                model_files=[]
            )
    
    def save(self):
        with open("system_profile.json", "w") as f:
            json.dump(self.dict(), f, indent=2)

# Global instance
SYSTEM_PROFILE = FPGASystemProfile.load()