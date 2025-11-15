from fastapi import Header, HTTPException, status
import re
from firebase_admin import auth
from .constants import EMAIL_REGEX, PASSWORD_REGEX


def validate_email(email: str):
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Invalid email format")


def validate_password(password: str):
    if not re.match(PASSWORD_REGEX, password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must be at least 8 characters long, contain an uppercase letter, "
                "a lowercase letter, a number, and a special character."
            ),
        )
    
async def get_decoded_token(authorization: str = Header(None)) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")

    id_token = authorization.split("Bearer ")[1]
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Firebase ID token")


# async def get_decoded_token(authorization: str = Header(None)) -> dict:
#     if authorization is None or not authorization.startswith("Bearer "):
#         raise HTTPException(status_code=401, detail="Missing Bearer token")

#     id_token = authorization.split(" ")[1]
#     try:
#         decoded_token = auth.verify_id_token(id_token)
#         return decoded_token
#     except Exception as e:
#         msg = str(e)
#         print("VERIFY ERROR:", repr(e))

#         # Если ошибка "Token used too early" — делаем проверку с допуском 5 секунд
#         if "Token used too early" in msg:
#             try:
#                 # Получаем публичные ключи Google
#                 keys = requests.get(
#                     "https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"
#                 ).json()

#                 header = jwt.get_unverified_header(id_token)
#                 public_key = keys[header["kid"]]

#                 # Повторная проверка с leeway
#                 decoded_token = jwt.decode(
#                     id_token,
#                     public_key,
#                     algorithms=["RS256"],
#                     audience=FIREBASE_PROJECT_ID,
#                     leeway=5
#                 )
#                 return decoded_token

#             except Exception as e2:
#                 print("SECOND VERIFY ERROR:", repr(e2))
#                 raise HTTPException(status_code=401, detail="Invalid token (after retry)")

#         raise HTTPException(status_code=401, detail="Invalid token")
