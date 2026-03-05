import asyncio
import subprocess
from typing import Dict, List

async def program_fpga(bitstream_path: str) -> Dict:
    # Check if hardware is available
    if not SYSTEM_PROFILE.hardware_inventory:
        return {
            "status": "skipped",
            "reason": "No FPGA hardware detected"
        }
    
    try:
        # Try to program FPGA using openocd
        result = subprocess.run([
            'openocd',
            '-c', f'interface ftdi',
            '-c', f'device_desc "Xilinx Platform Cable USB"',
            '-c', f'program {bitstream_path} verify'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            return {
                "status": "success",
                "message": "FPGA programmed successfully"
            }
        else:
            return {
                "status": "failed",
                "error": result.stderr
            }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }