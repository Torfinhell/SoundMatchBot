from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import get_db
from backend.models import User

router = APIRouter(prefix="/users", tags=["users"])

class RegisterReq(BaseModel):
    telegram_id: str
    username: str | None = None

@router.post("/register")
def register(req: RegisterReq, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(telegram_id=req.telegram_id).first()
    if not user:
        user = User(telegram_id=req.telegram_id, telegram_username=req.username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return {"user_id": user.id, "message": "ok"}