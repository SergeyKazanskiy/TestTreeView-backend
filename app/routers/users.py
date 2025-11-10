from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..services import crud
from ..schemas.user import User, UserCreate
from .. import models
from ..database import SessionLocal
from ..deps import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=List[User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)
