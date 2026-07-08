import numpy as np

class NREMPhase:
    def __init__(self, cognigraph, hebbian_threshold=0.3):
        """
        Executes structural consolidation and synaptic homeostatic regularization.
        """
        self.cognigraph = cognigraph
        self.threshold = hebbian_threshold
        print("[PHASE] NREM Phase Initialized.")

    def consolidate(self):
        """
        Replays episodic buffer, applies Hebbian learning, and extracts rules.
        """
        episodes = self.cognigraph.episodic.get_recent_episodes()
        
        # FIXED: Explicitly check for None or length 0 to avoid NumPy truth value ambiguity
        if episodes is None or episodes.get('embeddings') is None or len(episodes['embeddings']) == 0:
            print("[NREM] No episodes to consolidate.")
            return

        print(f"[NREM] Consolidating {len(episodes['embeddings'])} traces into Symbolic Schema...")
        embs = episodes['embeddings']
        docs = episodes['documents']
        metas = episodes['metadatas']

        # Hebbian Distillation
        for i in range(len(embs)):
            for j in range(i + 1, len(embs)):
                # Calculate semantic similarity
                sim = np.dot(embs[i], embs[j]) / (np.linalg.norm(embs[i]) * np.linalg.norm(embs[j]))
                
                if sim > self.threshold:
                    tag_a = metas[i]['tags'].split(',')[0] if metas[i]['tags'] else "ConceptA"
                    tag_b = metas[j]['tags'].split(',')[0] if metas[j]['tags'] else "ConceptB"
                    
                    if tag_a != tag_b:
                        context = f"{docs[i]} -> {docs[j]}"
                        self.cognigraph.route_to_semantic(tag_a, tag_b, float(sim), context)
        
        # Clear buffer to prevent proactive interference
        self.cognigraph.episodic.clear_buffer()