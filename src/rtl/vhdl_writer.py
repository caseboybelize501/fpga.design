from typing import List, Dict

async def generate_vhdl(module_name: str, function_type: str, primitives: List[str]) -> List[Dict]:
    # Generate VHDL code based on function type and available primitives
    if function_type == "multiplier":
        code = f"library ieee;\nuse ieee.std_logic_1164.all;\nuse ieee.numeric_std.all;\n\nentity {module_name} is\n    port (\n        a : in  std_logic_vector(31 downto 0);\n        b : in  std_logic_vector(31 downto 0);\n        result : out std_logic_vector(63 downto 0)\n    );\nend entity;\n\narchitecture rtl of {module_name} is\nbegin\n    result <= std_logic_vector(unsigned(a) * unsigned(b));\nend architecture;"
    elif function_type == "adder":
        code = f"library ieee;\nuse ieee.std_logic_1164.all;\nuse ieee.numeric_std.all;\n\nentity {module_name} is\n    port (\n        a : in  std_logic_vector(31 downto 0);\n        b : in  std_logic_vector(31 downto 0);\n        sum : out std_logic_vector(31 downto 0)\n    );\nend entity;\n\narchitecture rtl of {module_name} is\nbegin\n    sum <= std_logic_vector(unsigned(a) + unsigned(b));\nend architecture;"
    else:
        code = f"library ieee;\nuse ieee.std_logic_1164.all;\n\nentity {module_name} is\n    port (\n        clk : in  std_logic;\n        rst_n : in  std_logic;\n        data_in : in  std_logic_vector(31 downto 0);\n        data_out : out std_logic_vector(31 downto 0)\n    );\nend entity;\n\narchitecture rtl of {module_name} is\n    signal reg_data : std_logic_vector(31 downto 0);\nbegin\n    process(clk, rst_n)\n    begin\n        if rst_n = '0' then\n            reg_data <= (others => '0');\n        elsif rising_edge(clk) then\n            reg_data <= data_in;\n        end if;\n    end process;\n    \n    data_out <= reg_data;\nend architecture;"
    
    return [{
        "path": f"{module_name}.vhd",
        "content": code,
        "language": "vhdl"
    }]