from database import SessionLocal
from auth import decode_token
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session
from schemas.dbmodels import UserDB

user_schema = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token:str = Depends(user_schema), db:Session = Depends(get_db)):
    payload = decode_token(token)
    if payload is None or "email" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if payload.get("type")!="access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    else:
        user = db.query(UserDB).filter(UserDB.email == token["email"]).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User with that credentials no found")
        return user