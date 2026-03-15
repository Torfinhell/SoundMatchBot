import faiss
import numpy as np
import pickle
from pathlib import Path
from .config import settings

class FAISSWrapper:
    def __init__(self):
        self.dim = settings.backend.embedding_dim
        self.index = faiss.IndexFlatIP(self.dim)
        # Map: faiss_id -> (user_id, cluster_id)
        self.id_map = {} 
        self.counter = 0

    def add(self, user_id: int, cluster_id: int, embedding: np.ndarray):
        faiss.normalize_L2(embedding)
        self.index.add(embedding)
        self.id_map[self.counter] = (user_id, cluster_id)
        self.counter += 1

    def search(self, query: np.ndarray, k: int):
        faiss.normalize_L2(query)
        if self.index.ntotal == 0:
            return []
        scores, indices = self.index.search(query, k)
        return list(zip(indices[0], scores[0]))

    def save(self, path: str):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, path)
        with open(path + ".map", "wb") as f:
            pickle.dump(self.id_map, f)

    def load(self, path: str):
        if Path(path).exists():
            self.index = faiss.read_index(path)
            if Path(path + ".map").exists():
                with open(path + ".map", "rb") as f:
                    self.id_map = pickle.load(f)
                    self.counter = len(self.id_map)

# Global Instance
faiss_index = FAISSWrapper()