from database import SessionLocal
from schemas.dbmodels import IdempotencyKeyDB
from datetime import datetime,timezone

def auto_delete_row():
    db = SessionLocal()
    try:
        db.query(IdempotencyKeyDB).filter(IdempotencyKeyDB.expires_at < datetime.now(timezone.utc)).delete()
        db.commit()
    
    except Exception:
        db.rollback()
    finally:
        db.close()