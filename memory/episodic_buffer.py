import math
import time
import chromadb

class MetaController:
    def __init__(self, base_lambda=3600, base_tk=1.5):
        self.lambda_scale = base_lambda  # Time horizon (e.g., 3600 seconds)
        self.t_k = base_tk               # Shape parameter
        print(f"[SYSTEM] MetaController Initialized: t_k={self.t_k}, lambda={self.lambda_scale}")

    def update_decay_rates(self, recent_similarities):
        """
        Adjusts t_k based on environmental repetition.
        High similarity = Routine = Faster Decay (Higher t_k)
        Low similarity = Chaotic/Novel = Slower Decay (Lower t_k)
        """
        if not recent_similarities:
            return

        avg_sim = sum(recent_similarities) / len(recent_similarities)
        
        # Adaptive Feedback Loop
        if avg_sim > 0.85:
            # Highly repetitive environment: Forget faster to save compute/space
            self.t_k = min(2.5, self.t_k + 0.1)
        elif avg_sim < 0.50:
            # Novel or Chaotic environment: Retain data longer to learn
            self.t_k = max(0.5, self.t_k - 0.1)
            
        print(f"[METRICS] Env Similarity: {avg_sim:.2f} | Adaptive t_k updated to: {self.t_k:.2f}")


class EpisodicBuffer:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="wake_episodes",
            metadata={"hnsw:space": "cosine"}
        )
        # Instantiate the Adaptive Hypothalamus
        self.meta_controller = MetaController()
        print("[SYSTEM] Episodic Buffer Initialized with Adaptive Weibull-Decay.")

    def add_episode(self, raw_text, vector, tags, reward=0):
        timestamp = str(time.time())
        self.collection.add(
            documents=[raw_text],
            embeddings=[vector],
            metadatas=[{"tags": ",".join(tags), "reward": reward}],
            ids=[f"ep_{timestamp}"]
        )
        return f"ep_{timestamp}"
        
    def retrieve_with_weibull_decay(self, query_vector, n_results=5):
        """
        Executes R(t) = S_sem * w(Delta tau) with dynamic parameters.
        """
        count = self.collection.count()
        if count == 0:
            return []
            
        fetch_limit = min(count, n_results * 3)
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=fetch_limit,
            include=['documents', 'distances']
        )
        
        current_time = time.time()
        reranked_results = []
        recent_similarities = []
        
        for i in range(len(results['ids'][0])):
            doc_id = results['ids'][0][i]
            document = results['documents'][0][i]
            
            distance = results['distances'][0][i]
            s_sem = max(0.0, 1.0 - distance)
            recent_similarities.append(s_sem)
            
            try:
                encoded_time = float(doc_id.split('_')[1])
                delta_tau = current_time - encoded_time
            except (IndexError, ValueError):
                delta_tau = 0.0
                
            # Apply Adaptive Weibull Decay
            w_tau = math.exp(-((delta_tau / self.meta_controller.lambda_scale) ** self.meta_controller.t_k))
            r_t = s_sem * w_tau
            
            reranked_results.append({
                "document": document,
                "relevance_score": r_t,
                "s_sem": s_sem,
                "w_tau": w_tau
            })
            
        # Trigger Phase 1 self-regulation based on the context of this retrieval
        self.meta_controller.update_decay_rates(recent_similarities)
            
        reranked_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return reranked_results[:n_results]