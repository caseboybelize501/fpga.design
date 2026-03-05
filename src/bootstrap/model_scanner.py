import os
import hashlib
from typing import List, Dict

async def scan_models() -> List[Dict]:
    model_files = []
    
    # Standard paths to check
    standard_paths = [
        "/models",
        "/opt/models",
        "./models",
        os.path.expanduser("~/models"),
        os.path.expanduser("~/.cache/models")
    ]
    
    # Check inference servers
    server_ports = [11434, 8000, 1234, 8080]
    
    for port in server_ports:
        try:
            import httpx
            response = httpx.get(f"http://localhost:{port}/", timeout=5)
            if response.status_code == 200:
                model_files.append({
                    "type": "inference_server",
                    "port": port,
                    "status": "active"
                })
        except Exception as e:
            pass
    
    # Scan for GGUF files in standard paths
    for path in standard_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.gguf'):
                        full_path = os.path.join(root, file)
                        try:
                            # Calculate SHA256
                            with open(full_path, 'rb') as f:
                                file_hash = hashlib.sha256(f.read()).hexdigest()
                            
                            model_files.append({
                                "path": full_path,
                                "name": file,
                                "type": "gguf",
                                "sha256": file_hash
                            })
                        except Exception as e:
                            print(f"Error reading {full_path}: {e}")
    
    return model_files