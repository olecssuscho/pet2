from schemas.dbmodels import UserDB
from sqlalchemy.orm import Session

def block_user_services(id:int,db:Session):
    db.query(UserDB).filter(UserDB.id == id).first().is_blocked = True
    db.commit()
    return "Success"

def unblock_user_services(id:int,db:Session):
    db.query(UserDB).filter(UserDB.id == id).first().is_blocked = False
    db.commit()
    return "Success"