import os
import google.generativeai as genai

class REMPhase:
    def __init__(self, cognigraph):
        """
        Active Dreaming phase for counterfactual rule verification using Gemini.
        """
        self.cognigraph = cognigraph
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if api_key:
            genai.configure(api_key=api_key)
            self.llm = genai.GenerativeModel('gemini-3.5-flash')
            print("[PHASE] REM Phase (Gemini LLM Sandbox) Initialized.")
        else:
            self.llm = None
            print("[WARNING] GEMINI_API_KEY not found. REM phase will auto-verify.")

    def active_dreaming(self):
        """
        Tests hypothetical scenarios to synthesize generalized schemas.
        """
        unverified_rules = self.cognigraph.semantic.get_unverified_rules()
        if not unverified_rules:
            print("[REM] No new rules to validate.")
            return

        print(f"[REM] Active Dreaming... Validating {len(unverified_rules)} candidate rules.")
        
        for u, v, data in unverified_rules:
            if not self.llm:
                self.cognigraph.semantic.mark_rule_verified(u, v)
                continue
                
            prompt = (
                f"You are the 'Active Dreaming' module of an AI agent. "
                f"I have extracted a logical rule connecting the concept '{u}' to '{v}'. "
                f"Counterfactual simulation: What if '{u}' was suddenly completely unavailable or broken in the environment? "
                f"Would a relationship to '{v}' still logically hold to solve a problem? "
                f"Provide a 1-sentence reasoning, then answer strictly with YES or NO at the end."
            )
            
            response = self.llm.generate_content(prompt)
            print(f"      [Dream Simulation] {u} -> {v}: {response.text.strip()}")
            
            if "YES" in response.text.upper():
                self.cognigraph.semantic.mark_rule_verified(u, v)
                print(f"      [RESULT] Rule {u}->{v} Verified and Committed.")
            else:
                print(f"      [RESULT] Rule {u}->{v} Pruned (Failed Counterfactual).")
                # Prune the brittle rule from the graph
                self.cognigraph.semantic.graph.remove_edge(u, v)