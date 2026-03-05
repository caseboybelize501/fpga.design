import os
import subprocess
from typing import List, Dict

async def scan_device_libraries() -> Dict:
    device_libs = {
        "vivado": [],
        "quartus": [],
        "yosys": []
    }
    
    # Vivado Board Files
    vivado_path = os.environ.get('XILINX_VIVADO')
    if vivado_path:
        board_files_dir = os.path.join(vivado_path, "../../../data/boards/board_files")
        if os.path.exists(board_files_dir):
            for root, dirs, files in os.walk(board_files_dir):
                for file in files:
                    if file.endswith('.board'):
                        board_path = os.path.join(root, file)
                        try:
                            with open(board_path, 'r') as f:
                                content = f.read()
                                # Extract board name and part
                                device_libs["vivado"].append({
                                    "name": file.replace('.board', ''),
                                    "path": board_path,
                                    "content": content[:1000]  # First 1000 chars
                                })
                        except Exception as e:
                            print(f"Error reading Vivado board file {board_path}: {e}")
    
    # Quartus Device Info
    quartus_path = os.environ.get('QUARTUS_ROOTDIR')
    if quartus_path:
        devinfo_dir = os.path.join(quartus_path, "../quartus/common/devinfo")
        if os.path.exists(devinfo_dir):
            for root, dirs, files in os.walk(devinfo_dir):
                for file in files:
                    if file.endswith('.xml'):
                        devinfo_path = os.path.join(root, file)
                        try:
                            with open(devinfo_path, 'r') as f:
                                content = f.read()
                                device_libs["quartus"].append({
                                    "name": file,
                                    "path": devinfo_path,
                                    "content": content[:1000]
                                })
                        except Exception as e:
                            print(f"Error reading Quartus devinfo {devinfo_path}: {e}")
    
    # Yosys Targets
    try:
        result = subprocess.run(['yosys', '-p', 'help'], capture_output=True, text=True)
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'synth_' in line and 'target' in line:
                    target = line.strip()
                    device_libs["yosys"].append({
                        "name": target,
                        "description": "Yosys synthesis target"
                    })
    except Exception as e:
        print(f"Error scanning Yosys targets: {e}")
    
    return device_libs