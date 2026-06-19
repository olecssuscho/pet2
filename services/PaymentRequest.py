from schemas.dbmodels import PaymentRequestDB,UserDB
from sqlalchemy.orm import Session
from fastapi import status,HTTPException

def payment_request_services(email:str,payment_request:PaymentRequestDB,db:Session):
    user_email = db.query(UserDB).filter(UserDB.email == email).first()
    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    if db.query(UserDB).filter(UserDB.email == payment_request.from_user_email).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" Sender not found")
    
    if db.query(UserDB).filter(UserDB.email == payment_request.to_user_email).first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=" Receiver not found")
    
    if payment_request.amount<0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Sender amount less than 0 ")
    
    from_id = db.query(UserDB).filter(UserDB.email==payment_request.from_user_email).first().id
    to_id = db.query(UserDB).filter(UserDB.email==payment_request.to_user_email).first().id
    payment_request_db = PaymentRequestDB(
        from_user_id = from_id,
        to_user_id = to_id,
        from_user_email = payment_request.from_user_email,
        to_user_email = payment_request.to_user_email,
        amount = payment_request.amount,
        message = payment_request.message,
        status = "success",
        asker = email
    )
    db.add(payment_request_db)
    db.commit()

    return payment_request_db.status
    
