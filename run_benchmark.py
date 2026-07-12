import requests
import time
import random
import csv
from datetime import datetime

EDGE_WAKE_URL = "http://localhost:80/simulate_day"
CLOUD_SYNC_URL = "http://localhost:80/initiate_sync"

SCENARIOS = [
    {"text": "Drone engine activated.", "tags": ["system", "startup"]},
    {"text": "Drone lifted off the ground.", "tags": ["physics", "movement"]},
    {"text": "Drone reached cruising altitude.", "tags": ["physics", "movement"]},
    {"text": "Window shattered into pieces.", "tags": ["damage", "physics"]},
    {"text": "Drone crashed into the window.", "tags": ["collision", "physics"]},
    {"text": "Battery level dropped below 10%.", "tags": ["system", "power"]},
    {"text": "Emergency landing protocol initiated.", "tags": ["system", "safety"]},
    {"text": "Drone landed safely on the grass.", "tags": ["physics", "landing"]},
]

def generate_telemetry_batch(batch_size=50):
    batch = []
    for _ in range(batch_size):
        batch.append(random.choice(SCENARIOS))
    return batch

def run_experiment():
    print("🚀 Initiating SCNS Enterprise Multi-Model Benchmark Suite...")
    
    PROVIDERS = ["openai", "gemini", "ollama"]
    telemetry_data = generate_telemetry_batch(batch_size=100)
    
    for provider in PROVIDERS:
        print(f"\n======================================")
        print(f"🧪 INITIALIZING ABLATION TEST: {provider.upper()}")
        print(f"======================================")
        
        # WAKE PHASE: Encode real data into the Edge
        start_time = time.time()
        response = requests.post(EDGE_WAKE_URL, json=telemetry_data)
        edge_latency = time.time() - start_time
        if response.status_code == 200:
            print(f"✅ Edge Encoded Data in {edge_latency:.3f} seconds.")
        else:
            print("❌ Edge Node Failed")
            continue

        # SLEEP PHASE: Trigger Graph Pruning
        print(f"Triggering Sleep Cycle for {provider.upper()}...")
        start_time = time.time()
        
        # Route provider command through the load balancer
        response = requests.post(f"{CLOUD_SYNC_URL}?provider={provider}")
        
        cloud_latency = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            rules = data.get("rules_added", [])
            print(f"✅ {provider.upper()} Sync Complete in {cloud_latency:.3f} seconds.")
            print(f"🧠 Extracted {len(rules)} distinct physical rules.")
            
            filename = f"scns_benchmark_{provider}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Provider", "Edge_Latency_Sec", "Cloud_Latency_Sec", "Total_Events", "Verified_Rules_Count", "Rule_Text"])
                
                first_rule = rules[0] if rules else "None"
                writer.writerow([provider.upper(), round(edge_latency, 3), round(cloud_latency, 3), len(telemetry_data), len(rules), first_rule])
                
                for r in rules[1:]:
                    writer.writerow(["", "", "", "", "", r])
                    
            print(f"💾 {provider.upper()} data saved to {filename}")
        else:
            print(f"❌ {provider.upper()} Sync Failed: {response.status_code}")

if __name__ == "__main__":
    run_experiment()