from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..deps import get_db


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.User)
def register_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user_data)

@router.post("/login", response_model=schemas.User)
def login_user(user_data: schemas.UserLogin, db: Session = Depends(get_db)):
    return crud.authenticate_user(db, user_data.email, user_data.password)

@router.post("/logout")
def logout_user():
    return {"message": "Logged out successfully"}
