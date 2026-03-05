import subprocess
import usb.core
from typing import List, Dict

async def scan_hardware() -> List[Dict]:
    hardware = []
    
    # Use lsusb to detect FPGA programmers
    try:
        result = subprocess.run(['lsusb'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        for line in lines:
            if '0403:6010' in line or '09FB:6001' in line or '0403:6014' in line:
                # Parse device info
                parts = line.split()
                vendor_id = parts[5].split(':')[0] if len(parts) > 5 else "unknown"
                product_id = parts[5].split(':')[1] if len(parts) > 5 else "unknown"
                
                # Identify device type
                device_type = "unknown"
                if '0403:6010' in line:
                    device_type = "Digilent JTAG" if '0403' in line else "Gowin JTAG"
                elif '09FB:6001' in line:
                    device_type = "Intel USB Blaster"
                elif '0403:6014' in line:
                    device_type = "Xilinx Platform Cable"
                
                hardware.append({
                    "vendor_id": vendor_id,
                    "product_id": product_id,
                    "type": device_type,
                    "interface": "JTAG",
                    "confirmed_alive": True
                })
    except Exception as e:
        print(f"Error scanning hardware: {e}")
    
    # Try to probe with openocd
    try:
        result = subprocess.run(['openocd', '-c', 'adapter list'], capture_output=True, text=True)
        if result.returncode == 0:
            print("OpenOCD found and working")
    except Exception as e:
        print(f"Error with OpenOCD: {e}")
    
    return hardware