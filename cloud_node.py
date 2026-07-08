from fastapi import FastAPI, Request
import networkx as nx
import time
import requests

app = FastAPI(title="SCNS Cloud - Sleep Consolidation Engine")

class NREMGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()
        
    def extract_causal_rules(self, episodes):
        if len(episodes) < 2:
            return []
            
        print(f"[NREM] Extracting causal DAG from {len(episodes)} sequential episodes...")
        raw_rules = []
        
        for i in range(len(episodes) - 1):
            cause_node = episodes[i]
            effect_node = episodes[i+1]
            
            self.graph.add_edge(cause_node, effect_node, weight=1.0)
            rule = f"IF [{cause_node}] THEN [{effect_node}]"
            raw_rules.append((cause_node, effect_node, rule))
            
        return raw_rules

class REMSandbox:
    def __init__(self, nrem_graph):
        self.knowledge_graph = nrem_graph
        self.ollama_url = "http://localhost:11434/api/generate"
        
    def validate_and_prune(self, candidate_rules):
        print("\n[REM]  💭 Entering Active Dreaming Sandbox (Local LLM Validation)...")
        verified_rules = []
        
        for cause, effect, rule_text in candidate_rules:
            print(f"[REM]  Testing candidate: {rule_text}")
            
            # The strict zero-shot prompt engineered for the LLM
            prompt = f"""You are a strict physics and chronology validation engine.
Evaluate this causal rule: '{rule_text}'

You must apply these two absolute physical laws:
1. The Law of Linear Time: An effect (e.g., breaking, shattering, getting wet) CANNOT physically occur before its initiating cause (e.g., dropping, hitting, raining). 
2. The Law of Non-Circularity: An event cannot cause itself.

If the rule violates either of these laws, it is impossible. 
Respond strictly with exactly one word: 'VALID' or 'INVALID'."""

            try:
                # Fire the rule to your local Llama 3 model
                response = requests.post(
                    self.ollama_url,
                    json={
                        "model": "llama3",
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.0} # Zero creativity, maximum logic
                    }
                )
                
                if response.status_code == 200:
                    # Clean the AI's response (LLMs sometimes add periods or spaces)
                    llm_reply = response.json().get("response", "").strip().upper()
                    print(f"       🧠 LLM Reasoned: {llm_reply}")
                    
                    if "INVALID" in llm_reply:
                        print(f"       ❌ FAILED: Causal paradox detected. Pruning edge from graph.")
                        if self.knowledge_graph.graph.has_edge(cause, effect):
                            self.knowledge_graph.graph.remove_edge(cause, effect)
                    else:
                        print(f"       ✅ PASSED: Rule is structurally sound.")
                        verified_rules.append("VERIFIED: " + rule_text)
                else:
                    print(f"       ⚠️ API Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                print("       ⚠️ ERROR: Cannot connect to Ollama. Is the desktop app running?")
                
        return verified_rules

knowledge_graph = NREMGraphBuilder()
rem_sandbox = REMSandbox(knowledge_graph)

@app.post("/trigger_sleep")
async def process_sleep_cycle(request: Request):
    data = await request.json()
    agent_id = data.get("agent_id")
    episodes = data.get("episodes", [])
    
    print(f"\n[CLOUD] 🌙 Received Sleep Request from {agent_id}")
    
    print("\n[CLOUD] 🧠 NREM Phase: Mapping vectors to Global Knowledge Graph...")
    time.sleep(1) 
    raw_candidates = knowledge_graph.extract_causal_rules(episodes)
    
    time.sleep(1)
    verified_rules = rem_sandbox.validate_and_prune(raw_candidates)
    
    final_dispatch = list(set(verified_rules))
    
    print("\n[CLOUD] ✅ Sleep Cycle Complete. Dispatching verified logic to edge.")
    return {"status": "success", "consolidated_rules": final_dispatch}