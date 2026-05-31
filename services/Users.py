from schemas.dbmodels import UserDB
from sqlalchemy.orm import Session
from schemas.responces import UserResponce

def register_service(user:UserDB,db:Session) -> UserResponce:
    user_db=UserDB(**user.model_dump())
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

