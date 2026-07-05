from sentence_transformers import SentenceTransformer

class WakePhase:
    def __init__(self, cognigraph):
        """
        Fast-access episodic encoding into a short-term buffer.
        """
        self.cognigraph = cognigraph
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        print("[PHASE] Wake Phase Initialized.")

    def observe(self, text_observation, semantic_tags):
        """
        Extracts continuous vector representations from sensory inputs and buffers them.
        """
        print(f"[WAKE] Encoding episode: {text_observation}")
        vector = self.encoder.encode(text_observation).tolist()
        return self.cognigraph.route_to_episodic(text_observation, vector, semantic_tags)