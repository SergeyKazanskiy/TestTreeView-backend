from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from .firebase_admin_ import firebase_auth
from typing import Dict

router = APIRouter(prefix="/auth", tags=["auth"])

class CreateCustomTokenRequest(BaseModel):
    user_id: str  # идентификатор юзера на бэкенде или произвольный uid
    # можно добавить дополнительные проверки / авторизацию (например, пароли)

@router.post("/custom-token")
def create_custom_token(payload: CreateCustomTokenRequest):
    """
    Создаёт Firebase Custom Token для client-side signInWithCustomToken.
    В реальном приложении — убедись, что requester авторизован на сервере и имеет право получить токен для указанного user_id.
    """
    user_id = payload.user_id
    try:
        token_bytes = firebase_auth.create_custom_token(user_id)
        # create_custom_token returns bytes in older versions -> decode if necessary
        if isinstance(token_bytes, bytes):
            token = token_bytes.decode("utf-8")
        else:
            token = token_bytes
        return {"customToken": token}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create custom token")
