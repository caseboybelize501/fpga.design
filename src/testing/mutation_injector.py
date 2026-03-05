from typing import Dict, List

async def inject_timing_mutation(mutation_type: str) -> Dict:
    # Inject timing mutations for testing
    if mutation_type == "tighten_clock":
        return {
            "type": "tighten_clock",
            "description": "Tighten clock by 10%",
            "effect": "Design must still meet timing"
        }
    elif mutation_type == "add_hold_violations":
        return {
            "type": "add_hold_violations",
            "description": "Add hold violations via timing exceptions",
            "effect": "Must detect"
        }
    elif mutation_type == "increase_fanout":
        return {
            "type": "increase_fanout",
            "description": "Increase fanout on critical path",
            "effect": "Measure degradation"
        }
    else:
        return {
            "type": "unknown",
            "description": "Unknown mutation type"
        }