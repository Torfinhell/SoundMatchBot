from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..services.matching import Matcher

router = APIRouter(tags=["recommendations"])

@router.get("/recommendations/{user_id}")
def recommend(user_id: int, limit: int = 20, db: Session = Depends(get_db)):
    return Matcher(db).get_recommendations(user_id, limit)

@router.get("/leaderboard")
def leaderboard(limit: int = 20, db: Session = Depends(get_db)):
    # Mock leaderboard for demo using ID 1 as seed
    return Matcher(db).get_recommendations(1, limit)