import os
# CRITICAL FIX: Prevent PyTorch from clashing with Uvicorn asyncio on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI
import requests
from memory.episodic_buffer import EpisodicBuffer
from sentence_transformers import SentenceTransformer

app = FastAPI(title="SCNS Edge - Agent Wake Node")
buffer = EpisodicBuffer()

# 1. Load the real embedding model into Edge memory
print("\n[EDGE] 🧠 Loading deep learning embedding model (all-MiniLM-L6-v2)...")
encoder = SentenceTransformer('all-MiniLM-L6-v2')
print("[EDGE] ✅ Model loaded and ready.")

CLOUD_URL = "http://localhost:8080/trigger_sleep"

@app.post("/simulate_day")
def simulate_day():
    print("\n[EDGE] ☀️ Waking up. Gathering daily episodes...")
    
    # Raw textual events (no more hardcoded math vectors)
    events = [
        ("User dropped the glass.", ["physics"]),
        ("Glass shattered on floor.", ["physics", "damage"]),
        ("User dropped the glass.", ["physics"]) # The paradox
    ]
    
    # 2. Dynamically encode text into 384-dimensional semantic vectors
    for text, tags in events:
        real_vector = encoder.encode(text).tolist()
        buffer.add_episode(text, real_vector, tags)
        print(f"       -> Encoded & Buffered: '{text}' (Vector Size: {len(real_vector)})")
    
    return {"status": "Day complete, real vectors buffered."}

@app.post("/initiate_sync")
def initiate_sync():
    print("\n[EDGE] 🔋 Battery low / Day ended. Initiating Cloud Sync...")
    
    episodes = buffer.collection.get(include=['documents', 'embeddings', 'metadatas'])
    
    payload = {
        "agent_id": "Edge_Drone_Alpha",
        "episodes": episodes['documents'] 
    }
    
    try:
        response = requests.post(CLOUD_URL, json=payload)
        
        if response.status_code == 200:
            cloud_data = response.json()
            print(f"[EDGE] 📥 Downloaded verified logic rules from Cloud:")
            for rule in cloud_data['consolidated_rules']:
                print(f"       {rule}")
            
            # 3. Physically wipe the short-term buffer for the next day
            # (Assuming clear_buffer() or similar logic handles deletion in episodic_buffer.py)
            buffer.client.delete_collection("wake_episodes")
            buffer.collection = buffer.client.get_or_create_collection(
                name="wake_episodes",
                metadata={"hnsw:space": "cosine"}
            )
            print("[EDGE] 🧹 Local buffer cleared. Ready for a new day.")
            return {"status": "Sync successful", "rules_added": cloud_data['consolidated_rules']}
            
    except requests.exceptions.ConnectionError:
        print("[EDGE] ❌ ERROR: Could not connect to Cloud. Sleep delayed.")
        return {"error": "Cloud unreachable"}