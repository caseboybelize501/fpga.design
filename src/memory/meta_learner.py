from typing import Dict, List
import numpy as np
from sklearn.linear_model import LinearRegression

# In-memory meta-learning index
META_LEARNER_INDEX = {
    "approach_performance": {},
    "device_timing": {}
}

async def update_meta_learning_index(data: Dict):
    # Update meta-learning index with new data
    approach = data['design_approach']
    device = data['device_family']
    freq = data['freq_target']
    cycles = data['cycles_to_stable']
    
    key = f"{approach}_{device}_{freq}"
    if key not in META_LEARNER_INDEX["approach_performance"]:
        META_LEARNER_INDEX["approach_performance"][key] = []
    
    META_LEARNER_INDEX["approach_performance"][key].append(cycles)

async def query_meta_learning(approach: str, device: str, freq: int) -> Dict:
    # Query meta-learning for best approach
    key = f"{approach}_{device}_{freq}"
    if key in META_LEARNER_INDEX["approach_performance"]:
        cycles_list = META_LEARNER_INDEX["approach_performance"][key]
        avg_cycles = np.mean(cycles_list)
        return {
            "recommended_approach": approach,
            "expected_cycles": avg_cycles,
            "confidence": len(cycles_list) / 10.0  # Normalize to 0-1
        }
    
    return {
        "recommended_approach": "default",
        "expected_cycles": 5,
        "confidence": 0.1
    }