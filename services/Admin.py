from schemas.dbmodels import UserDB,TransactionDB
from sqlalchemy.orm import Session
from sqlalchemy import func

def block_user_services(id:int,db:Session):
    db.query(UserDB).filter(UserDB.id == id).first().is_blocked = True
    db.commit()
    return "Success"

def unblock_user_services(id:int,db:Session):
    db.query(UserDB).filter(UserDB.id == id).first().is_blocked = False
    db.commit()
    return "Success"

def get_transactions_services(db:Session):
    return db.query(TransactionDB).all()

def get_transactions_stats_services(db:Session):
    count = db.query(TransactionDB).count()
    sum_amount = db.query(func.sum(TransactionDB.amount)).scalar()
    return {"count":count,"sum":sum_amount}