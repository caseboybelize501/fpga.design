import asyncio
from src.bootstrap.eda_scanner import scan_eda_tools
from src.bootstrap.device_library_scanner import scan_device_libraries
from src.bootstrap.hardware_scanner import scan_hardware
from src.bootstrap.model_scanner import scan_models
from src.bootstrap.system_profile import FPGASystemProfile

async def scan_system():
    print("Starting system scan...")
    
    # Phase 1: EDA Toolchain Scan
    eda_tools = await scan_eda_tools()
    
    # Phase 2: Device Library Scan
    device_libs = await scan_device_libraries()
    
    # Phase 3: Hardware Scan
    hardware_inventory = await scan_hardware()
    
    # Phase 4: Model Files Scan
    model_files = await scan_models()
    
    # Create system profile
    profile = FPGASystemProfile(
        eda_toolchain=eda_tools,
        device_libraries=device_libs,
        hardware_inventory=hardware_inventory,
        model_files=model_files
    )
    
    # Save profile
    profile.save()
    print("System scan complete.")