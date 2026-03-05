from typing import Dict, List
import chromadb

# ChromaDB client for timing failure storage
client = chromadb.Client()

async def store_timing_failure(failure_data: Dict):
    # Store timing failure in ChromaDB
    try:
        collection = client.get_or_create_collection("timing_failures")
        
        collection.add(
            documents=[f"RTL construct: {failure_data['rtl_construct']}, Device: {failure_data['device_family']}",],
            metadatas=[failure_data],
            ids=[f"failure_{hash(str(failure_data)) % 1000000}"]
        )
    except Exception as e:
        print(f"Error storing timing failure: {e}")

async def query_timing_failures(device_family: str, clock_freq_mhz: int) -> List[Dict]:
    # Query timing failures for device family and frequency
    try:
        collection = client.get_collection("timing_failures")
        results = collection.query(
            query_texts=[f"Device: {device_family}, Frequency: {clock_freq_mhz} MHz"],
            n_results=5
        )
        return results['metadatas']
    except Exception as e:
        print(f"Error querying timing failures: {e}")
        return []