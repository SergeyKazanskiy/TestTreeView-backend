import os
import firebase_admin
from firebase_admin import credentials, auth
from config import SECRETS_DIR


KEY_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", SECRETS_DIR / "firebase-key.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(KEY_PATH)
    firebase_admin.initialize_app(cred)

firebase_auth = auth
