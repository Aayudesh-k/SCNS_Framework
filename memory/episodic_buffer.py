import chromadb
import time

class EpisodicBuffer:
    def __init__(self, persist_directory="./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(
            name="wake_episodes",
            metadata={"hnsw:space": "cosine"}
        )
        print("[SYSTEM] Episodic Buffer (ChromaDB) Initialized.")

    def add_episode(self, raw_text, vector, tags, reward=0):
        timestamp = str(time.time())
        self.collection.add(
            documents=[raw_text],
            embeddings=[vector],
            metadatas=[{"tags": ",".join(tags), "reward": reward}],
            ids=[f"ep_{timestamp}"]
        )
        return f"ep_{timestamp}"

    def get_recent_episodes(self, limit=100):
        count = self.collection.count()
        if count == 0:
            return []
        return self.collection.get(include=['embeddings', 'documents', 'metadatas'])
        
    def clear_buffer(self):
        self.client.delete_collection("wake_episodes")
        self.collection = self.client.create_collection(
            name="wake_episodes",
            metadata={"hnsw:space": "cosine"}
        )
        print("[SYSTEM] Episodic Buffer Cleared for next Wake Cycle.")