from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict
from backend.database import get_db
from backend.models import Poll, PollAnswer
from backend.config import settings

router = APIRouter(prefix="/polls", tags=["polls"])

class PollReq(BaseModel):
    title: str
    questions: List[str]
    admin_password: str

class AnswerReq(BaseModel):
    user_id: int
    answers: Dict[str, str]

@router.post("")
def create_poll(req: PollReq, db: Session = Depends(get_db)):
    if req.admin_password != settings.backend.admin_password:
        raise HTTPException(403, "Invalid Password")
    poll = Poll(title=req.title, questions=req.questions, created_by_admin_id=1) 
    db.add(poll)
    db.commit()
    return {"poll_id": poll.id}

@router.get("/active")
def get_active(db: Session = Depends(get_db)):
    polls = db.query(Poll).filter_by(is_active=True).all()
    return [{"id": p.id, "title": p.title, "questions": p.questions} for p in polls]

@router.post("/{poll_id}/submit")
def submit(poll_id: int, req: AnswerReq, db: Session = Depends(get_db)):
    existing = db.query(PollAnswer).filter_by(user_id=req.user_id, poll_id=poll_id).first()
    if existing:
        existing.answers = req.answers
    else:
        new_ans = PollAnswer(user_id=req.user_id, poll_id=poll_id, answers=req.answers)
        db.add(new_ans)
    db.commit()
    return {"status": "submitted"}