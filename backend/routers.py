from fastapi import APIRouter, Depends, HTTPException, status
from backend.database import get_db
from sqlalchemy.orm import Session
from backend.models import User

router = APIRouter()


@router.get("/")
async def root(db: Session = Depends(get_db)):
    response = db.query(User).all()
    return response
