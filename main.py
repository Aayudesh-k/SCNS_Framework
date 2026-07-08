import numpy as np
import time
from memory.episodic_buffer import EpisodicBuffer

def run_wake_phase():
    # Initialize the framework
    buffer = EpisodicBuffer()
    
    print("\n--- Starting Wake Phase (Routine Encoding) ---")
    
    # 1. Agent experiences an event
    vector_a = np.array([0.1, 0.2, 0.3]).tolist()
    buffer.add_episode("User dropped the glass.", vector_a, ["physics", "glass"])
    
    # Force a delay so Weibull Delta Tau > 0
    print("[SYSTEM] Simulating time passing...")
    time.sleep(2) 
    
    # 2. Agent encounters a highly routine/repetitive situation
    print("\n[AGENT] Querying Memory: 'Glass is falling' (Routine)")
    vector_query = np.array([0.1, 0.22, 0.31]).tolist() # High cosine similarity
    
    # This automatically triggers retrieval AND adjusts the MetaController
    results = buffer.retrieve_with_weibull_decay(vector_query, n_results=1)
    
    for r in results:
        print(f"Retrieved: '{r['document']}' | Score: {r['relevance_score']:.3f} | Current t_k: {buffer.meta_controller.t_k:.2f}")

    # 3. Agent suddenly encounters a novel/chaotic situation
    print("\n[AGENT] Querying Memory: 'A spaceship just landed' (Chaotic/Novel)")
    vector_novel = np.array([0.9, -0.5, 0.8]).tolist() # Low cosine similarity
    
    results = buffer.retrieve_with_weibull_decay(vector_novel, n_results=1)
    
    for r in results:
         print(f"Retrieved: '{r['document']}' | Score: {r['relevance_score']:.3f} | Current t_k: {buffer.meta_controller.t_k:.2f}")

if __name__ == "__main__":
    run_wake_phase()