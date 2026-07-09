import math
import time
import psycopg2
from pgvector.psycopg2 import register_vector
import os

class MetaController:
    def __init__(self, base_lambda=3600, base_tk=1.5):
        self.lambda_scale = base_lambda
        self.t_k = base_tk
        print(f"[SYSTEM] MetaController Initialized: t_k={self.t_k}, lambda={self.lambda_scale}")

    def update_decay_rates(self, recent_similarities):
        if not recent_similarities:
            return
        avg_sim = sum(recent_similarities) / len(recent_similarities)
        
        if avg_sim > 0.85:
            self.t_k = min(2.5, self.t_k + 0.1)
        elif avg_sim < 0.50:
            self.t_k = max(0.5, self.t_k - 0.1)
            
        print(f"[METRICS] Env Similarity: {avg_sim:.2f} | Adaptive t_k updated to: {self.t_k:.2f}")

class EpisodicBuffer:
    def __init__(self):
        # Connect to the Postgres container via Docker network
        self.db_url = os.getenv("DATABASE_URL", "postgresql://scns_user:securepassword@db:5432/scns_db")
        self._setup_db()
        self.meta_controller = MetaController()
        print("[SYSTEM] Enterprise Episodic Buffer Initialized (PostgreSQL + pgvector).")

    def _setup_db(self):
        time.sleep(3) 
        self.conn = psycopg2.connect(self.db_url)
        self.conn.autocommit = True
        
        with self.conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            register_vector(self.conn)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS wake_episodes (
                    id VARCHAR PRIMARY KEY,
                    document TEXT,
                    embedding vector(384),
                    tags TEXT,
                    encoded_time FLOAT
                );
            """)

    def add_episode(self, raw_text, vector, tags, reward=0):
        timestamp = time.time()
        ep_id = f"ep_{timestamp}"
        
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO wake_episodes (id, document, embedding, tags, encoded_time) VALUES (%s, %s, %s, %s, %s)",
                (ep_id, raw_text, vector, ",".join(tags), timestamp)
            )
        return ep_id
        
    def retrieve_with_weibull_decay(self, query_vector, n_results=5):
        current_time = time.time()
        
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT document, 1 - (embedding <=> %s::vector) AS s_sem, encoded_time 
                FROM wake_episodes 
                ORDER BY embedding <=> %s::vector 
                LIMIT %s
            """, (query_vector, query_vector, n_results * 3))
            
            results = cur.fetchall()

        reranked_results = []
        recent_similarities = []
        
        for doc, s_sem, encoded_time in results:
            recent_similarities.append(s_sem)
            delta_tau = current_time - encoded_time
            w_tau = math.exp(-((delta_tau / self.meta_controller.lambda_scale) ** self.meta_controller.t_k))
            r_t = s_sem * w_tau
            
            reranked_results.append({
                "document": doc,
                "relevance_score": r_t
            })
            
        self.meta_controller.update_decay_rates(recent_similarities)
        reranked_results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return reranked_results[:n_results]

    # --- THE NEW POSTGRES EXTRACTION FUNCTION ---
    def get_all_episodes(self):
        """Fetches all daily events in chronological order for the NREM Graph"""
        with self.conn.cursor() as cur:
            cur.execute("SELECT document FROM wake_episodes ORDER BY encoded_time ASC;")
            results = cur.fetchall()
            return [row[0] for row in results]

    def clear_buffer(self):
        with self.conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE wake_episodes;")