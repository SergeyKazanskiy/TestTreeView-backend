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