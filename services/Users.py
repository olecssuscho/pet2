from schemas.dbmodels import UserDB
from sqlalchemy.orm import Session
from schemas.responces import UserResponce
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException,status
from auth import verify_password,create_access_token,create_refresh_token,hash_password

def register_service(user:UserDB,db:Session) -> UserResponce:
    refresh_token=create_refresh_token({"email":user.email})
    newpassword=hash_password(user.password)
    user.password=newpassword
    db.add(UserDB(**user.model_dump(),refresh_token=refresh_token))
    db.commit()
    return refresh_token

def login_services(form_data:OAuth2PasswordRequestForm,db:Session):
    user = db.query(UserDB).filter(UserDB.email==form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not verify_password(form_data.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is not correct")
    access_token = create_access_token({"email": user.email})
    return {"access_token": access_token, "refresh_token": user.refresh_token,"token_type": "bearer"}
    