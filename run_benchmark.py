import requests
import time
import random
import csv
from datetime import datetime

# Target the Nginx Load Balancer
EDGE_WAKE_URL = "http://localhost:80/simulate_day"
CLOUD_SYNC_URL = "http://localhost:80/initiate_sync"

# A dataset of logical and illogical physics events
SCENARIOS = [
    # Logical Sequence
    {"text": "Drone engine activated.", "tags": ["system", "startup"]},
    {"text": "Drone lifted off the ground.", "tags": ["physics", "movement"]},
    {"text": "Drone reached cruising altitude.", "tags": ["physics", "movement"]},
    
    # Intentional Temporal Paradox (Effect before Cause)
    {"text": "Window shattered into pieces.", "tags": ["damage", "physics"]},
    {"text": "Drone crashed into the window.", "tags": ["collision", "physics"]},
    
    # Independent Causal Chain
    {"text": "Battery level dropped below 10%.", "tags": ["system", "power"]},
    {"text": "Emergency landing protocol initiated.", "tags": ["system", "safety"]},
    {"text": "Drone landed safely on the grass.", "tags": ["physics", "landing"]},
]

def generate_telemetry_batch(batch_size=50):
    """Generates a massive list of randomized events to stress-test the Edge Node."""
    batch = []
    for _ in range(batch_size):
        batch.append(random.choice(SCENARIOS))
    return batch

def run_experiment():
    print("🚀 Initiating SCNS Enterprise Benchmark Suite...")
    
    # 1. GENERATE DATA
    telemetry_data = generate_telemetry_batch(batch_size=100) # Sending 100 events
    
    # 2. TEST EDGE NODE (Sub-Symbolic Encoding Load)
    print(f"\n[TEST 1] Blasting Load Balancer with {len(telemetry_data)} physical events...")
    start_time = time.time()
    
    response = requests.post(EDGE_WAKE_URL, json=telemetry_data)
    
    edge_latency = time.time() - start_time
    if response.status_code == 200:
        print(f"✅ Edge Node successfully encoded {len(telemetry_data)} vectors in {edge_latency:.3f} seconds.")
    else:
        print(f"❌ Edge Node Failed: {response.text}")
        return

    # 3. TEST CLOUD NODE (LLM Reasoning Load)
    print("\n[TEST 2] Triggering Sleep Cycle. Forcing LLM to parse structural graph...")
    start_time = time.time()
    
    response = requests.post(CLOUD_SYNC_URL)
    
    cloud_latency = time.time() - start_time
    
    if response.status_code == 200:
        data = response.json()
        rules = data.get("rules_added", [])
        print(f"✅ Cloud Sync Complete in {cloud_latency:.3f} seconds.")
        print(f"🧠 Llama 3 validated and extracted {len(rules)} distinct physical rules.")
        print("\n--- Verified Global Rules ---")
        for r in rules:
            print(f"   {r}")
            
        # --- SAVE DATA TO CSV ---
        filename = f"scns_benchmark_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Edge_Latency_Sec", "Cloud_Latency_Sec", "Total_Events", "Verified_Rules_Count", "Rule_Text"])
            
            # Write the metrics row, putting the first rule in the same line
            first_rule = rules[0] if rules else "None"
            writer.writerow([round(edge_latency, 3), round(cloud_latency, 3), len(telemetry_data), len(rules), first_rule])
            
            # Write the rest of the rules underneath
            for r in rules[1:]:
                writer.writerow(["", "", "", "", r])
                
        print(f"\n💾 Benchmark data successfully saved to {filename}")
    else:
        print(f"❌ Cloud Sync Failed: {response.status_code}")

if __name__ == "__main__":
    run_experiment()