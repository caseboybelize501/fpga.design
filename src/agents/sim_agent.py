import asyncio
import subprocess
from typing import Dict, List
from src.testing.sim_runner import run_verilator_simulation, run_iverilog_simulation

async def run_simulation(rtl_files: List[Dict], constraints: Dict) -> Dict:
    # Run behavioral simulation with Verilator or Icarus
    try:
        # Try Verilator first
        result = await run_verilator_simulation(rtl_files)
        if result['success']:
            return {
                "simulator": "verilator",
                "status": "passed",
                "assertions_passed": result['assertions_passed'],
                "waveform_path": result['waveform_path']
            }
    except Exception as e:
        print(f"Verilator simulation failed: {e}")
    
    # Fall back to Icarus
    try:
        result = await run_iverilog_simulation(rtl_files)
        if result['success']:
            return {
                "simulator": "iverilog",
                "status": "passed",
                "assertions_passed": result['assertions_passed'],
                "waveform_path": result['waveform_path']
            }
    except Exception as e:
        print(f"Icarus simulation failed: {e}")
    
    return {
        "simulator": "none",
        "status": "failed",
        "error": "No simulation tool succeeded"
    }