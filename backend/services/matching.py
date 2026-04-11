import numpy as np
from sqlalchemy.orm import Session
from backend.models import User, PollAnswer
from backend.faiss_index import faiss_index
from backend.config import settings
from backend.services.embedding import embedding_extractor

class Matcher:
    def __init__(self, db: Session):
        self.db = db
    
    def text_based_filter(self, user_id: int, top_k: int) -> list:
        # Simplified Jaccard similarity on answers for demo
        # Real implementation would use TF-IDF as per architecture docs
        target_answers = self.db.query(PollAnswer).filter_by(user_id=user_id).all()
        target_set = set()
        for ans in target_answers:
            target_set.update(ans.answers.values())
        
        candidates = []
        others = self.db.query(User).filter(User.id != user_id).all()
        for other in others:
            o_answers = self.db.query(PollAnswer).filter_by(user_id=other.id).all()
            o_set = set()
            for ans in o_answers:
                o_set.update(ans.answers.values())
            
            if not target_set and not o_set:
                score = 0
            else:
                score = len(target_set & o_set) / len(target_set | o_set) if (target_set | o_set) else 0
            candidates.append((other.id, score))
        
        candidates.sort(key=lambda x: x[1], reverse=True)
        return [c[0] for c in candidates[:top_k]]

    def music_based_rerank(self, user_id: int, candidates: list) -> list:
        # In a real implementation, extract embeddings from user-uploaded audio
        # using embedding_extractor.extract(audio_path), then search FAISS
        # For demo, we use random embeddings
        results = []
        for cid in candidates:
            # Mock similarity score
            results.append((cid, np.random.random()))
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def get_recommendations(self, user_id: int, limit: int):
        candidates = self.text_based_filter(user_id, settings.backend.num_people_refilter)
        ranked = self.music_based_rerank(user_id, candidates)
        
        output = []
        for rank, (uid, score) in enumerate(ranked[:limit], 1):
            u = self.db.query(User).filter_by(id=uid).first()
            output.append({
                "user_id": uid, 
                "username": u.telegram_username, 
                "score": float(score), 
                "rank": rank
            })
        return output