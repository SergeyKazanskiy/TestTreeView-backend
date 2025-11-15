from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_session
from schemas.user import UserCreate, UserLogin, RegistrationResponse, LoginResponse
from models.users import User
from auth.utils import validate_email, validate_password
import firebase_admin
from firebase_admin import auth, credentials
from pathlib import Path
#import bcrypt


firebase_key_path = Path("../secrets/firebase-key.json")
if not firebase_key_path.is_file():
    raise RuntimeError(f"{firebase_key_path} not found")

cred = credentials.Certificate(str(firebase_key_path))
firebase_admin.initialize_app(cred)


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegistrationResponse)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_session)):
    validate_email(user_data.email)
    validate_password(user_data.password)

    result = await db.execute(select(User).filter(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    #hashed_password = bcrypt.hashpw(user_data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=user_data.password, #hashed_password
        token_FCM=""
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = auth.create_custom_token(f"user_{new_user.id}")
    return {"user_id": new_user.id, "token": token}


@router.post("/login")
async def login_user(user_data: UserLogin, db: AsyncSession = Depends(get_session)):
    validate_email(user_data.email)
    validate_password(user_data.password)

    query = select(User).where(User.email == user_data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=400, detail="No account found with this email")

    # if not bcrypt.checkpw(user_data.password.encode("utf-8"), user.password.encode("utf-8")):
    if user.password != user_data.password:
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token = auth.create_custom_token(f"user_{user.id}")
    return {"user_id": user.id, "token": token, "first_name": user.first_name, "last_name": user.last_name}


@router.post("/logout")
def logout_user():
    return {"message": "Logged out successfully"}

