from schemas.dbmodels import User
from sqlalchemy.orm import Session
from schemas.responces import UserResponce

def register_service(user:User,db:Session) -> UserResponce:
    user_db=User(**user.model_dump())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

