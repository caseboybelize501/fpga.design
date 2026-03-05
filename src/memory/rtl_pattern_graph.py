from typing import Dict, List
import neo4j

# Neo4j driver for RTL pattern graph
driver = neo4j.Driver("bolt://localhost:7687", auth=("neo4j", "password"))

async def query_rtl_patterns(function_type: str, device_family: str) -> List[Dict]:
    # Query Neo4j for RTL patterns that meet timing
    try:
        with driver.session() as session:
            result = session.run(
                "MATCH (r:RTLConstruct)-[:MEETS_TIMING_AT]->(d:DeviceFamily {name: $device}) WHERE r.type = $type RETURN r.name, d.name LIMIT 10",
                type=function_type,
                device=device_family
            )
            
            patterns = []
            for record in result:
                patterns.append({
                    "construct": record["r.name"],
                    "device": record["d.name"]
                })
            
            return patterns
    except Exception as e:
        print(f"Error querying RTL patterns: {e}")
        return []

async def store_rtl_pattern(pattern_data: Dict):
    # Store new RTL pattern in Neo4j
    try:
        with driver.session() as session:
            session.run(
                "MERGE (r:RTLConstruct {name: $name}) SET r.type = $type RETURN r.name",
                name=pattern_data['name'],
                type=pattern_data['type']
            )
    except Exception as e:
        print(f"Error storing RTL pattern: {e}")