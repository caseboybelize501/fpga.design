from typing import List, Dict

async def generate_xdc(module_name: str) -> str:
    # Generate XDC constraints for Xilinx devices
    return f"# Clock constraint\ncreate_clock -period 10.0 [get_ports clk]\n\n# Pin assignments\nset_property -dict {{PACKAGE_PIN A12 IOSTANDARD LVCMOS33}} [get_ports data_in]
set_property -dict {{PACKAGE_PIN B12 IOSTANDARD LVCMOS33}} [get_ports data_out]
\n# Timing constraints\nset_multicycle_path -from [get_clocks clk] -to [get_clocks clk] 2"

async def generate_sdc(module_name: str) -> str:
    # Generate SDC constraints for Intel devices
    return f"# Clock constraint\ncreate_clock -period 10.0 [get_ports clk]\n\n# Pin assignments\nset_instance_assignment -name IO_STANDARD LVCMOS33 -to data_in
set_instance_assignment -name IO_STANDARD LVCMOS33 -to data_out
\n# Timing constraints\nset_multicycle_path -from [get_clocks clk] -to [get_clocks clk] 2"