from dependency import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from schemas.dbmodels import IdempotencyKeyDB
from datetime import datetime,timezone

def auto_delete_row(db:Session = Depends(get_db)):
    try:
        db.query(IdempotencyKeyDB).filter(IdempotencyKeyDB.expires_at < datetime.now(timezone.utc)).delete()
        db.commit()
    
    except Exception:
        db.rollback()