from sqlalchemy.orm import Session

from ..schemas import user
from .. import models

def get_users(db: Session):
    return db.query(models.User).all()

def create_user(db: Session, user: user.UserCreate):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
