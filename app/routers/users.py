from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_session
from services.crud import CRUD
from schemas.user import UserResponse, UserCreate
from models.users import User


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_session)):
    return db.query(User).all()

@router.post("/", response_model=User)
def create_user(user_data: UserCreate, db: Session = Depends(get_session)):
    new_user = User(name=user_data.name, email=user_data.email, password=user_data.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_update.name
    db.commit()
    db.refresh(user)
    return user