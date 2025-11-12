from pydantic import BaseModel

class UserBase(BaseModel):
    first_name: str
    last_name: str

class UserCreate(UserBase):
    email: str
    password: str
    
class UserLogin(BaseModel):
    email: str
    password: str

class RegistrationResponse(BaseModel):
    id: int
    token: str

class LoginResponse(UserBase):
    id: int
    token: str

    class Config:
        orm_mode = True
        
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class TokenUpdate(BaseModel):
    token_FCM: str