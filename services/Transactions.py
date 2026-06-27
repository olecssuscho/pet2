from schemas.dbmodels import UserDB,TransactionDB,WebhookDB
from schemas.responces import TransactionResponceGood
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import status,HTTPException,BackgroundTasks
from services.Webhook import post_webhook_on_url
import validators
from datetime import timezone,datetime

def transaction_service(backgroundtask:BackgroundTasks,email:str,transaction:TransactionDB,reciever_email,db:Session) -> TransactionResponceGood:

    try:
        sender_db = db.query(UserDB).filter(UserDB.email==email).with_for_update().first()
        if not sender_db:
            bad_transaction_db = TransactionDB(
            attempted_sender_id = None, 
            amount = transaction.amount,
            status = "failed",
            type = transaction.type,
            attempted_sender_email = email,
            attempted_reciever_email = reciever_email,
            asker = email
            )
            db.add(bad_transaction_db)
            db.commit()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Sender not found")
        if sender_db.is_blocked:
            bad_transaction_db = TransactionDB(
            sender_id = sender_db.id,
            amount = transaction.amount,
            status = "frozen",
            type = transaction.type,
            attempted_sender_email = email,
            attempted_reciever_email = reciever_email,
            asker = email
            )
            db.add(bad_transaction_db)
            db.commit()
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Sender blocked")
        
        reciever_db = db.query(UserDB).filter(UserDB.email==reciever_email).with_for_update().first()
        if not reciever_db:   
            bad_transaction_db = TransactionDB(
            sender_id = sender_db.id,
            attempted_reciever_id = None,
            amount = transaction.amount,
            status = "failed",
            type = transaction.type,
            attempted_sender_email = email,
            attempted_reciever_email = reciever_email,
            asker = email
            )
            db.add(bad_transaction_db)
            db.commit()
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Receiver not found")
        if reciever_db.is_blocked:    
            bad_transaction_db = TransactionDB(
            sender_id = sender_db.id,
            reciever_id  = reciever_db.id,
            amount = transaction.amount,
            status = "frozen",
            type = transaction.type,
            attempted_sender_email = email,
            attempted_reciever_email = reciever_email,
            asker = email
            )
            db.add(bad_transaction_db)
            db.commit()
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Receiver blocked")
        
        sender_amount = transaction.amount
        
        if sender_db.balance < sender_amount or sender_amount < 0:     
            bad_transaction_db = TransactionDB(
            sender_id = sender_db.id,
            reciever_id = reciever_db.id,
            amount = transaction.amount,
            status = "failed",
            type = transaction.type,
            attempted_sender_email = email,
            attempted_reciever_email = reciever_email,
            asker = email
            )
            db.add(bad_transaction_db)
            db.commit()
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,detail="Sender amount less than 0 or less than balance")
        
        db.query(UserDB).filter(UserDB.email==email).update({UserDB.balance: UserDB.balance - sender_amount})
        db.query(UserDB).filter(UserDB.email==reciever_email).update({UserDB.balance: UserDB.balance + sender_amount})
    
        transaction_db = TransactionDB( 
            sender_id = sender_db.id,
            reciever_id  = reciever_db.id,
            amount = transaction.amount,
            status = "success",
            type = transaction.type,
            attempted_sender_email = email,
            attempted_reciever_email = reciever_email,
            asker = email
            )
        db.add(transaction_db)
        db.commit()
        db.refresh(transaction_db)

        webhook = db.query(WebhookDB).filter(WebhookDB.user_id == sender_db.id).first()
        if webhook is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = " Your Webhook is not found") 

        if validators.url(webhook.url) is False:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = " Your URL is not worked")
        else:
            backgroundtask.add_task(post_webhook_on_url,webhook.url,transaction_db.status,sender_db.id,db)
            backgroundtask.add_task(post_webhook_on_url,webhook.url,transaction_db.status,reciever_db.id,db)


    except HTTPException:
        raise

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f"Content: {e}")

    return transaction_db


def get_transactions_services(user:UserDB,db:Session):
    return db.query(TransactionDB).filter((TransactionDB.sender_id == user.id) | ((TransactionDB.reciever_id == user.id))).all()


def get_particular_transaction_services(id:int,user:UserDB,db:Session):
    transaction = db.query(TransactionDB).filter(TransactionDB.id == id,(TransactionDB.sender_id == user.id) | (TransactionDB.reciever_id == user.id)).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return transaction

def delete_transaction_services(id:int,user:UserDB,db:Session):
    to_delete = db.query(TransactionDB).filter(TransactionDB.id == id).first()
    to_delete.deleted_at = datetime.now(timezone.utc)
    db.commit()
    return "Success"