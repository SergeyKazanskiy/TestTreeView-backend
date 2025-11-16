from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession 
from typing import List
from database import get_session
from services.crud import CRUD
from schemas.shared import ResponseId, ResponseOk
from schemas.user import UserResponse, UserCreate, UserUpdate
from models.users import User
from sqlalchemy.future import select


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=List[UserResponse])
def get_users(db: AsyncSession = Depends(get_session)):
    return CRUD.get(User, db)

@router.post("/", response_model=ResponseId)
def create_user(data: UserCreate, db: AsyncSession = Depends(get_session)):
    return CRUD.add(User, data, db)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=ResponseOk)
def update_user(user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_session)):
    return CRUD.update(User, user_id, data, db)