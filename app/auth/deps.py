from fastapi import Header, HTTPException, status
from firebase_admin import auth as fb_auth


async def get_decoded_token(authorization: str = Header(None)) -> dict:
    """
    Проверяет Firebase ID токен, полученный в заголовке:
    Authorization: Bearer <idToken>
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

    id_token = authorization.split("Bearer ")[1]
    try:
        decoded_token = fb_auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase ID token")
