import asyncio
from fastapi import FastAPI, HTTPException
from src.bootstrap.system_scanner import scan_system
from src.planner.fpga_planner import plan_design
from src.agents.rtl_agent import generate_rtl
from src.agents.synth_agent import run_synthesis
from src.testing.cycle_manager import run_validation_cycle
from src.bootstrap.system_profile import FPGASystemProfile

app = FastAPI(title="FPGA Design Jarvis", version="0.1.0")

@app.on_event("startup")
async def startup_event():
    print("Starting FPGA Design Jarvis...")
    await scan_system()
    print("System scan complete.")

@app.get("/api/system/profile")
async def get_system_profile():
    try:
        profile = FPGASystemProfile.load()
        return profile.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/design/start")
async def start_design(function_description: str):
    try:
        design_id = await plan_design(function_description)
        return {"design_id": design_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/design/{design_id}/cycle")
async def get_cycle_results(design_id: str):
    try:
        results = await run_validation_cycle(design_id)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    try:
        profile = FPGASystemProfile.load()
        return {
            "eda_detected": len(profile.eda_toolchain) > 0,
            "hardware_connected": len(profile.hardware_inventory) > 0,
            "consecutive_passes": profile.consecutive_passes,
            "memory_hit_rate": profile.memory_hit_rate
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)