from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.database import get_db
from backend.models import User
from backend.config import settings

router = APIRouter(prefix="/admin", tags=["admin"])

class ClaimReq(BaseModel):
    user_id: int
    password: str

@router.post("/claim")
def claim_admin(req: ClaimReq, db: Session = Depends(get_db)):
    if req.password != settings.backend.admin_password:
        return {"success": False, "message": "Invalid password"}
    user = db.query(User).filter_by(id=req.user_id).first()
    if user:
        user.is_admin = True
        db.commit()
    return {"success": True, "message": "Admin claimed"}