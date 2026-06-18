from schemas.dbmodels import RefundDB,TransactionDB,UserDB
from sqlalchemy.orm import Session
from fastapi import status,HTTPException


def refund_services(refund:RefundDB,db:Session):
    transaction_db = db.query(TransactionDB).filter(TransactionDB.id==refund.transaction_id).first()
    if transaction_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="This Transaction does not exist")
    
    refund_db = db.query(RefundDB).filter(RefundDB.transaction_id==refund.transaction_id).first()
    if refund_db:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="This Refund exist")
    
    if transaction_db.status!="success":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Only successful transactions can be refunded")
    
    #important part

    sender_db = db.query(UserDB).filter(UserDB.id==transaction_db.sender_id).with_for_update().first()
    receiver_db = db.query(UserDB).filter(UserDB.id==transaction_db.reciever_id).with_for_update().first()

    sender_db_balance = sender_db.balance + transaction_db.amount
    receiver_db_balance = receiver_db.balance - transaction_db.amount  
    
    if sender_db_balance<0:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Sender amount less than 0 or less than balance")

    if receiver_db_balance<0:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Receiver amount less than 0 or less than balance")
    
    sender_db.balance = sender_db_balance
    receiver_db.balance = receiver_db_balance
   
    refund_db = RefundDB(
        transaction_id = refund.transaction_id,
        reason = refund.reason,
        status = "success"
    )
    db.add(refund_db)
    db.commit() 
    return refund_db.status
    
