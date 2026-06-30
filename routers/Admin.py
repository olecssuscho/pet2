from schemas.models import UserMODEL
from sqlalchemy.orm import Session
from fastapi import Depends,APIRouter
from dependency import get_db,get_current_admin
from services.Admin import block_user_services,unblock_user_services,get_transactions_services,get_transactions_stats_services

router = APIRouter(prefix="/admin", tags=["Admins"])

@router.post("/user/{id}/block")
def block_user(id: int, admin: UserMODEL = Depends(get_current_admin), db: Session = Depends(get_db)):
    return block_user_services(id,db)

@router.post("/user/{id}/unblock")
def unblock_user(id: int, admin: UserMODEL = Depends(get_current_admin), db: Session = Depends(get_db)):
    return unblock_user_services(id,db)

@router.get("/transactions")
def get_transactions(admin: UserMODEL = Depends(get_current_admin), db: Session = Depends(get_db)):
    return get_transactions_services(db)

@router.get("/stats")
def get_transactions_stats(admin: UserMODEL = Depends(get_current_admin), db: Session = Depends(get_db)):
    return get_transactions_stats_services(db)