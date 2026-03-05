import asyncio
from src.bootstrap.system_profile import SYSTEM_PROFILE
from src.agents.rtl_agent import generate_rtl
from src.agents.constraint_agent import generate_constraints
from src.agents.sim_agent import run_simulation
from src.agents.synth_agent import run_synthesis
from src.agents.timing_agent import analyze_timing
from src.agents.hw_agent import program_fpga
from src.agents.learn_agent import update_memory

async def plan_design(function_description: str) -> str:
    design_id = f"design_{hash(function_description) % 1000000}"
    
    # Get device family from system profile
    device_family = SYSTEM_PROFILE.device_libraries.vivado[0].get('family') if SYSTEM_PROFILE.device_libraries.vivado else "unknown"
    
    # Generate RTL
    rtl_result = await generate_rtl(function_description, device_family)
    
    # Generate constraints
    constraint_result = await generate_constraints(rtl_result['module_name'], device_family)
    
    # Run simulation
    sim_result = await run_simulation(rtl_result['files'], constraint_result)
    
    # Run synthesis
    synth_result = await run_synthesis(rtl_result['files'], constraint_result)
    
    # Analyze timing
    timing_result = await analyze_timing(synth_result['timing_report'])
    
    # Program FPGA if available
    if SYSTEM_PROFILE.hardware_inventory:
        hw_result = await program_fpga(synth_result['bitstream_path'])
    
    # Update memory
    await update_memory(rtl_result, timing_result)
    
    return design_id