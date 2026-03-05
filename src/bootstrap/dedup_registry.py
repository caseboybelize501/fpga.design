import hashlib
from typing import List, Dict

# Registry for deduplicating EDA tools, IP cores, and model files
DEDUP_REGISTRY = {
    "tools": {},
    "ip_cores": {},
    "model_files": {}
}

async def register_tool(tool_info: Dict):
    key = f"{tool_info['tool']}_{tool_info['version']}"
    if key not in DEDUP_REGISTRY["tools"]:
        DEDUP_REGISTRY["tools"][key] = tool_info
        return True
    return False

async def register_ip_core(core_info: Dict):
    key = core_info.get('sha256') or core_info.get('name', '')
    if key not in DEDUP_REGISTRY["ip_cores"]:
        DEDUP_REGISTRY["ip_cores"][key] = core_info
        return True
    return False

async def register_model_file(file_info: Dict):
    key = file_info.get('sha256') or file_info.get('path', '')
    if key not in DEDUP_REGISTRY["model_files"]:
        DEDUP_REGISTRY["model_files"][key] = file_info
        return True
    return False