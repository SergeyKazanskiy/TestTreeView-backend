from .database import SessionLocal

def get_db():
    """Общая зависимость для работы с БД"""
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
