from sqlalchemy import Connection, event, inspect
from database import SessionLocal
from schemas.dbmodels import AuditLogDB, UserDB
from sqlalchemy.orm import Mapper

@event.listens_for(UserDB,"before_update")
def audit_logppp_before(mapper:Mapper,conn:Connection,target:UserDB):
    state = inspect(target)
    history = state.attrs.balance.history
    if history.deleted:
        target._old_balance = history.deleted[0]

@event.listens_for(UserDB,"after_update")
def audit_logppp_after(mapper:Mapper,conn:Connection,target:UserDB):
    old_balance_db = getattr(target,"_old_balance",None)
    if old_balance_db is None or old_balance_db == target.balance:
        return
    
    conn.execute(AuditLogDB.__table__.insert().values(user_id = target.id,
            old_balance = old_balance_db,
            new_balance = target.balance,
            changed_by = getattr(target,"_changed_by","unknown"),
            reason = getattr(target,"_reason","unknown")))
       


