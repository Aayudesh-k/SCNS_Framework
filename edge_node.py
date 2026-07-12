import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from fastapi import FastAPI
import requests
from memory.episodic_buffer import EpisodicBuffer
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel
from typing import List

app = FastAPI(title="SCNS Edge - Agent Wake Node")
buffer = EpisodicBuffer()

print("\n[EDGE] 🧠 Loading deep learning embedding model (all-MiniLM-L6-v2)...")
encoder = SentenceTransformer('all-MiniLM-L6-v2')
print("[EDGE] ✅ Model loaded and ready.")

CLOUD_URL = "http://cloud_node:8080/trigger_sleep"

class Episode(BaseModel):
    text: str
    tags: List[str]

@app.post("/simulate_day")
def simulate_day(episodes: List[Episode]):
    print(f"\n[EDGE] ☀️ Waking up. Processing {len(episodes)} dynamic episodes...")
    for ep in episodes:
        real_vector = encoder.encode(ep.text).tolist()
        buffer.add_episode(ep.text, real_vector, ep.tags)
    return {"status": f"Day complete, {len(episodes)} vectors buffered."}

@app.post("/initiate_sync")
def initiate_sync(provider: str = "ollama"):
    print(f"\n[EDGE] 🔋 Battery low. Initiating Cloud Sync with {provider.upper()}...")
    
    episodes = buffer.get_all_episodes()
    payload = {
        "agent_id": "Edge_Drone_Alpha",
        "episodes": episodes,
        "provider": provider
    }
    
    try:
        response = requests.post(CLOUD_URL, json=payload)
        
        if response.status_code == 200:
            cloud_data = response.json()
            print(f"[EDGE] 📥 Downloaded verified logic rules from Cloud:")
            for rule in cloud_data.get('consolidated_rules', []):
                print(f"       {rule}")
            
            buffer.clear_buffer() 
            print("[EDGE] 🧹 Local buffer cleared. Ready for a new day.")
            return {"status": "Sync successful", "rules_added": cloud_data.get('consolidated_rules', [])}
            
    except requests.exceptions.ConnectionError:
        print("[EDGE] ❌ ERROR: Could not connect to Cloud. Sleep delayed.")
        return {"error": "Cloud unreachable"}