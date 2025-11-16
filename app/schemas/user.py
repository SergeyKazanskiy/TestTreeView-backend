from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    first_name: str
    last_name: str
    token_FCM: Optional[str]

class UserCreate(UserBase):
    email: str
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]

class UserLogin(BaseModel):
    email: str
    password: str

class RegistrationResponse(BaseModel):
    user_id: int
    token: str


class LoginResponse(BaseModel):
    user_id: int
    token: str
    first_name: str
    last_name: str

        
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class TokenUpdate(BaseModel):
    token_FCM: str