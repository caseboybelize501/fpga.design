# FPGA Design Jarvis

Autonomous FPGA/Hardware Design System that writes HDL, synthesizes designs, runs timing simulation,
deploys to connected FPGAs, validates with a 10-stage hardware test cycle,
and builds a self-learning library of which RTL patterns meet timing
on which device families.

## The Space That Doesn't Exist

FPGA development is one of the last bastions of purely manual expert craft
in computing. The tools — Vivado, Quartus, Yosys, OpenROAD — are powerful
but arcane. The feedback loop is brutal: write RTL → synthesize (10-60
minutes) → place and route → timing analysis → often fail → back to RTL.
Every FPGA family (Xilinx Ultrascale+, Intel Agilex, Lattice ECP5, Gowin)
has different primitive libraries, timing constraints, IP cores, and toolchain
quirks. The self-learning opportunity is enormous: every timing failure teaches
something about how this logic maps to this fabric.

## System Architecture


STARTUP BOOTSTRAP (HARD PARAMS — ABSOLUTE FIRST):
┌─────┬──────────────────────────────────────────────────────────────────────┐
│ PHASE 1 — EDA TOOLCHAIN                                            │
│ → Vivado: $XILINX_VIVADO → vivado -version → parse version        │
│ → Quartus: $QUARTUS_ROOTDIR → quartus_sh --version                │
│ → Yosys: which yosys → yosys --version                            │
│ → OpenROAD: which openroad → openroad --version (for ASIC flow)   │
│ → Simulators: which verilator, which iverilog, which vsim         │
│ → Register: { tool, version, path, features: [], license_ok: bool} │
│                                                                    │
│ PHASE 2 — DEVICE LIBRARIES (dedup — never reinstall support pkgs) │
│ → Vivado: list board_files/ → extract { board_name, part, family } │
│ → Quartus: parse devinfo/ → device families available             │
│ → Yosys: list targets (synth_xilinx, synth_intel, synth_ecp5...) │
│ → IP catalog: Vivado IP catalog → list available cores + versions │
│ → sha256 hash per IP core → dedup registry                        │
│                                                                    │
│ PHASE 3 — CONNECTED HARDWARE (what is physically programmable)   │
│ → lsusb → match FPGA programmer VIDs:                            │
│   Digilent: 0403:6010 (FTDI-based JTAG)                         │
│   Altera USB Blaster: 09FB:6001                                   │
│   Xilinx Platform Cable: 0403:6014                                │
│   Gowin: 0403:6010 (shared VID)                                  │
│ → openocd -c "adapter list" → confirm JTAG adapters             │
│ → Write HardwareInventory: [{ board, interface, confirmed_alive }] │
│                                                                    │
│ PHASE 4 — MODEL FILES + INFERENCE (sha256 dedup)                │
│ → Standard paths + probe :11434 :8000 :1234 :8080               │
│ → Write FPGASystemProfile → VALIDATE → unlock agents            │
└─────┴──────────────────────────────────────────────────────────────────────┘

10-STAGE HARDWARE VALIDATION CYCLE:
┌─────┬──────────────────────────────────────────────────────────────────────┐
│ Stage 01 — Lint              : Verilator --lint-only 0 warnings   │
│ Stage 02 — Behavioral Sim   : all testbench assertions pass       │
│ Stage 03 — Code Coverage    : toggle + branch ≥ 90%              │
│ Stage 04 — Synthesis        : synthesizes without critical errors  │
│ Stage 05 — Timing (Setup)   : WNS ≥ 0 (no setup violations)     │
│ Stage 06 — Timing (Hold)    : WHS ≥ 0 (no hold violations)      │
│ Stage 07 — Resource Fit     : utilization ≤ 80% (LUT/FF/BRAM)   │
│ Stage 08 — Power Estimate   : on-chip power ≤ budget             │
│ Stage 09 — Hardware Test    : bitstream on FPGA passes IO tests  │
│            [Stage 09 skipped if no hardware in SystemProfile]    │
│ Stage 10 — Regression       : prior STABLE designs still meet    │
│                                                                    │
│ TIMING MUTATION TESTING (between cycles):                        │
│ → Tighten clock by 10% → design must still meet timing          │
│ → Add hold violations via timing exceptions → must detect        │
│ → Increase fanout on critical path → measure degradation         │
│ → Timing brittleness → RTL Agent targeted pipelining pass       │
│                                                                    │
│ STABLE GATE: 7 consecutive passing cycles across all 10 stages   │
└─────┴──────────────────────────────────────────────────────────────────────┘

## Stack

- Orchestrator: Python (FastAPI + asyncio)
- Planner LLM: routed via FPGASystemProfile.inference_config
- Voice input: faster-whisper (local)
- System scan: psutil + subprocess + usb.core + httpx
- RTL gen: custom Verilog/VHDL/SV template engine + LLaMA
- Simulation: Verilator (fast) + Icarus Verilog (compatibility)
- Synthesis: Vivado (subprocess: vivado -mode tcl) + Yosys (open)
- Timing parse: custom Vivado timing report parser (XML + text)
- JTAG program: openocd (subprocess) + Digilent Adept SDK (Python)
- Logic analyzer: sigrok Python API (if LA connected)
- Model scan: sha256 + GGUF parser
- Dedup registry: PostgreSQL (EDA tools + IP cores + model files)
- Memory RAG: ChromaDB (timing failures + RTL patterns)
- Timing graph: Neo4j (RTL construct → timing path → device → outcome)
- Meta-learner: sklearn (RTL style → device family → freq → cycles)
- Database: PostgreSQL (designs, constraints, synthesis runs, cycles)
- Queue: Celery + Redis (async synthesis + simulation jobs)
- Interface: React (design dashboard + timing visualizer + memory)

## Features

1. **Autonomous Design Flow**: End-to-end automation from function description to hardware deployment
2. **Self-Learning Memory**: Accumulates knowledge about which RTL patterns meet timing on which devices
3. **Multi-Toolchain Support**: Vivado, Quartus, Yosys support with automatic detection
4. **Hardware Validation**: 10-stage validation cycle with mutation testing
5. **Device-Aware Generation**: Uses correct primitives for each FPGA family
6. **Timing Intelligence**: Pre-pipelines known problematic paths based on memory
7. **Deduplication System**: Prevents reinstalling same tools/IP cores/model files
8. **Real-time Dashboard**: Web interface for monitoring design progress and timing analysis

## Quick Start

bash
# Clone the repository
$ git clone https://github.com/caseboybelize501/fpga.design
$ cd fpga.design

# Install dependencies
$ pip install -r requirements.txt

# Run system scan
$ python src/main.py

# Start API server
$ uvicorn src.main:app --host 0.0.0.0 --port 8000


## API Endpoints

- `GET /api/system/profile` → FPGASystemProfile
- `GET /api/eda/toolchain` → detected tools + versions
- `GET /api/hardware/boards` → connected FPGA boards
- `GET /api/ip/catalog` → available IP cores
- `POST /api/design/start` → function description → RTL pipeline
- `GET /api/design/:id/cycle` → all 10 stage results
- `GET /api/design/:id/timing` → timing report + critical paths
- `GET /api/design/:id/utilization` → resource usage breakdown
- `GET /api/memory/timing` → timing failure pattern library
- `GET /api/memory/rtl-patterns` → RTL → timing graph query
- `GET /api/memory/synthesis` → synthesis strategy library
- `GET /api/memory/meta` → timing closure meta stats
- `POST /api/hw/program` → JTAG program connected board
- `GET /health` → system health check

## License

MIT License
