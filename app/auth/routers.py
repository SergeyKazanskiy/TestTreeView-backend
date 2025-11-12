from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_session
from schemas.user import UserCreate, UserLogin, RegistrationResponse, LoginResponse
from models.users import User
from auth.utils import get_custom_token, validate_email, validate_password 
#import bcrypt


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegistrationResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_session)):
    validate_email(user_data.email)
    validate_password(user_data.password)

    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    #hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password #hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = get_custom_token(f"user_{new_user.id}")
    return RegistrationResponse(id=new_user.id, token=token)


@router.post("/login", response_model=LoginResponse)
def login_user(user_data: UserLogin, db: Session = Depends(get_session)):
    validate_email(user_data.email)
    validate_password(user_data.password)

    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # if not bcrypt.checkpw(user_data.password.encode("utf-8"), user.password.encode("utf-8")):
    if not user or user.password != user_data.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = get_custom_token(f"user_{user.id}")
    return LoginResponse(id=user.id, first_name=user.first_name, last_name=user.last_name, token=token)


@router.post("/logout")
def logout_user():
    return {"message": "Logged out successfully"}

