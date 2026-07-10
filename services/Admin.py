from schemas.dbmodels import UserDB,TransactionDB,BlacklistDB
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status,HTTPException

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

def block_ip_services(sendet_ip:str,sendet_reason:str,db:Session):
    BL = BlacklistDB(ip=sendet_ip,reason=sendet_reason)
    if db.query(BlacklistDB).filter(BL.ip == sendet_ip).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Ip alredy has banned")
    db.add(BL)
    db.commit()
    return BL

def unblock_ip_services(sendet_ip:str,db:Session):
    BL = db.query(BlacklistDB).filter(BlacklistDB.ip == sendet_ip).first()
    if BL is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Ip did not found")
    db.delete(BL)
    db.commit()
    return "Ip was unblocked"