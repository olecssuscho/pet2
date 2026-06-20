from schemas.dbmodels import UserDB,TransactionDB,RefundDB
from sqlalchemy.orm import Session
from schemas.responces import UserResponce
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException,status
from sqlalchemy import func,select
from auth import verify_password,create_access_token,create_refresh_token,hash_password
from auth import decode_token,create_access_token

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

def get_user_services(user:UserDB,db:Session):
    return db.query(UserDB).filter(UserDB.id==user.id).first()

def refresh_services(token:str,db:Session):
    refresh = decode_token(token)
    if not refresh:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    if not "email" in refresh:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    if refresh.get("type")!="refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")
    if db.query(UserDB).filter(UserDB.email == refresh["email"]).first():
        access = create_access_token({"email": refresh["email"]})
        return {"access_token": access, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
def get_stats_services(user:UserDB, db:Session):
    total_transactions =  db.query(TransactionDB).filter(TransactionDB.attempted_sender_email == user.email).count()
    total_refunds = db.query(RefundDB).filter(RefundDB.asker == user.email).count()
    total_sent = db.query(func.sum(TransactionDB.amount)).filter(TransactionDB.attempted_sender_email == user.email).scalar()
    total_recieve =db.query(func.sum(TransactionDB.amount)).filter( TransactionDB.attempted_reciever_email == user.email).scalar()
    return {"total_transactions":total_transactions , 
            "total_refunds": total_refunds , 
            "total_sent": total_sent, 
            "total_recieve":total_recieve}