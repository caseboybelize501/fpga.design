from typing import List, Dict

# Device family primitive mappings
PRIMITIVE_LIBRARY = {
    "xilinx_ultrascale": {
        "dsp": ["DSP48E2", "DSP48E1"],
        "bram": ["RAMB36E2", "RAMB18E2"],
        "uram": ["URAM288"],
        "clock": ["BUFGCE", "MMCME4"],
        "io": ["IOBUF", "IBUF", "OBUF"]
    },
    "intel_agilex": {
        "dsp": ["DSP block"],
        "bram": ["M20K BRAM"],
        "hyper_ram": ["HyperRAM"],
        "clock": ["FPLL"],
        "io": ["IOBUF", "IBUF", "OBUF"]
    },
    "lattice_ecp5": {
        "dsp": ["MULT18X18D"],
        "pll": ["EHXPLLL"],
        "dca": ["DCCA"],
        "bram": ["DP16KD"],
        "io": ["IOBUF", "IBUF", "OBUF"]
    },
    "gowin_gw2a": {
        "dsp": ["MULTADDALU18X18"],
        "bram": ["BSRAM"],
        "pll": ["rPLL"],
        "io": ["IOBUF", "IBUF", "OBUF"]
    }
}

async def get_primitives_for_family(device_family: str) -> List[str]:
    # Return primitives for the specified device family
    if device_family in PRIMITIVE_LIBRARY:
        primitives = []
        for category, items in PRIMITIVE_LIBRARY[device_family].items:
            primitives.extend(items)
        return primitives
    else:
        return []