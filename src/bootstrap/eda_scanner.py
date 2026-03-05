import subprocess
import os
from typing import List, Dict

async def scan_eda_tools() -> List[Dict]:
    tools = []
    
    # Vivado
    vivado_path = os.environ.get('XILINX_VIVADO')
    if vivado_path:
        try:
            result = subprocess.run([os.path.join(vivado_path, 'bin', 'vivado'), '-version'], 
                                  capture_output=True, text=True)
            version = result.stdout.split('\n')[0] if result.stdout else "unknown"
            tools.append({
                "tool": "vivado",
                "version": version,
                "path": vivado_path,
                "features": ["synthesis", "pnr", "timing_analysis"],
                "license_ok": True
            })
        except Exception as e:
            print(f"Error scanning Vivado: {e}")
    
    # Quartus
    quartus_path = os.environ.get('QUARTUS_ROOTDIR')
    if quartus_path:
        try:
            result = subprocess.run([os.path.join(quartus_path, 'bin', 'quartus_sh'), '--version'], 
                                  capture_output=True, text=True)
            version = result.stdout.split('\n')[0] if result.stdout else "unknown"
            tools.append({
                "tool": "quartus",
                "version": version,
                "path": quartus_path,
                "features": ["synthesis", "pnr", "timing_analysis"],
                "license_ok": True
            })
        except Exception as e:
            print(f"Error scanning Quartus: {e}")
    
    # Yosys
    try:
        result = subprocess.run(['yosys', '--version'], capture_output=True, text=True)
        version = result.stdout.split('\n')[0] if result.stdout else "unknown"
        tools.append({
            "tool": "yosys",
            "version": version,
            "path": "yosys",
            "features": ["synthesis", "logic_optimization"],
            "license_ok": True
        })
    except Exception as e:
        print(f"Error scanning Yosys: {e}")
    
    # Verilator
    try:
        result = subprocess.run(['verilator', '--version'], capture_output=True, text=True)
        version = result.stdout.split('\n')[0] if result.stdout else "unknown"
        tools.append({
            "tool": "verilator",
            "version": version,
            "path": "verilator",
            "features": ["simulation", "linting"],
            "license_ok": True
        })
    except Exception as e:
        print(f"Error scanning Verilator: {e}")
    
    # Icarus Verilog
    try:
        result = subprocess.run(['iverilog', '-V'], capture_output=True, text=True)
        version = result.stderr.split('\n')[0] if result.stderr else "unknown"
        tools.append({
            "tool": "iverilog",
            "version": version,
            "path": "iverilog",
            "features": ["simulation", "linting"],
            "license_ok": True
        })
    except Exception as e:
        print(f"Error scanning Icarus Verilog: {e}")
    
    return tools