import asyncio
from typing import Dict, List
from src.rtl.constraint_writer import generate_xdc, generate_sdc

async def generate_constraints(module_name: str, device_family: str) -> Dict:
    # Generate timing constraints based on device family and board info
    if device_family.startswith("xilinx"):
        constraints = generate_xdc(module_name)
        return {
            "type": "xdc",
            "content": constraints,
            "path": f"{module_name}.xdc"
        }
    else:
        constraints = generate_sdc(module_name)
        return {
            "type": "sdc",
            "content": constraints,
            "path": f"{module_name}.sdc"
        }